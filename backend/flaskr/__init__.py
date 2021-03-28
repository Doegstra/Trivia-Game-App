import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    # helper method to paginate questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={'/*': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Controll-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    # Endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=["GET"])
    def get_categories():

        formatted_categories = {
            cat.id: cat.type for cat in
            Category.query.order_by(Category.id).all()}

        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    # Endpoint to handle GET requests for questions, including pagination
    #  (every QUESTIONS_PER_PAGE questions).
    @app.route('/questions', methods=["GET"])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        # React frontend expects dictionary,
        # c.f. https://knowledge.udacity.com/questions/233578
        formatted_categories = {
            cat.id: cat.type for cat in
            Category.query.order_by(Category.id).all()}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': None
        })

    # Endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(422)

    # Endpoint to POST a new question
    @app.route('/questions', methods=["POST"])
    def create_new_question():
        body = request.get_json()
        try:
            new_question = Question(question=body.get('question'),
                                    answer=body.get('answer'),
                                    category=body.get('category'),
                                    difficulty=body.get('difficulty'))
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id
            })
        except Exception:
            abort(405)

    # Endpoint to get questions based on a search term
    @ app.route('/questions_search', methods=["POST"])
    def search_question():
        body = request.get_json()
        search = body.get('searchTerm')
        try:
            relevant_questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search))).all()

            # 404 if no results found
            if (len(relevant_questions) == 0):
                abort(404)

            formatted_questions = paginate_questions(
                request, relevant_questions)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(Question.query.all())
            })
        except Exception:
            abort(400)

    # Endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_for_category(category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if category is None:
            abort(422)

        questions = Question.query.order_by(Question.id).filter(
            Question.category == category_id).all()
        formatted_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(Question.query.all()),
            'current_category': category_id
        })

    # Endpoint to play the quiz
    @app.route('/quizzes', methods=["POST"])
    def play_quiz():
        body = request.get_json()
        category = body.get('quiz_category', None)
        category_id = category.get('id')
        previous_questions_ids = body.get('previous_questions', None)

        if category_id is None:
            abort(400)

        if category_id == 0:
            questions = Question.query.order_by(Question.id).all()
        elif len(Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()) > 0:
            questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()
        else:
            abort(404)

        # only take questions not in previous questions
        relevant_questions = [
            q for q in questions if q.id not in previous_questions_ids]

        if len(relevant_questions) > 0:
            next_question = random.choice(relevant_questions)
        else:  # if all questions have been played
            return jsonify({
                'success': True
            })

        return jsonify({
            'success': True,
            'question': next_question.format()
        })

    # 400 Bad Request: The server cannot or will not process the request due
    #  to an apparent client error (e.g., malformed request syntax, size too
    #  large, invalid request message framing, or deceptive request routing).

    @app.errorhandler(400)
    def error_bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    # 404 Not Found: The requested resource could not be found but may be
    #  available in the future.  Subsequent requests by the client are
    #  permissible.
    @ app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @ app.errorhandler(405)
    def error_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    # 422 Unprocessable Entity:
    # The request was well-formed but was unable to be followed due to
    #  semantic errors.
    @ app.errorhandler(422)
    def error_unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422

    return app
