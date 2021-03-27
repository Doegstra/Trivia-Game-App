import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):  # helper method to paginate questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins. TODO Delete the sample route after completing the TODOs
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})

    CORS(app)

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
            cat.id: cat.type for cat in Category.query.order_by(Category.id).all()}

        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    # Endpoint to handle GET requests for questions, including pagination (every QUESTIONS_PER_PAGE questions).
    @app.route('/questions', methods=["GET"])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        # React frontend expects dictionary, c.f. https://knowledge.udacity.com/questions/233578
        formatted_categories = {
            cat.id: cat.type for cat in Category.query.order_by(Category.id).all()}

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
        except:
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
        except:
            abort(405)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    # 404 Not Found: The requested resource could not be found but may be available in the future.
    # Subsequent requests by the client are permissible.
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
    # The request was well-formed but was unable to be followed due to semantic errors.
    @ app.errorhandler(422)
    def error_unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422

    return app
