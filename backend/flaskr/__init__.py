import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.header.add('Access-Controll-Allow-Headers',
                            'Content-Type,Authorization,true')
        response.header.add('Access-Controll-Allow-Methods',
                            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=["GET"])
    def get_categories():

        formatted_categories = [category.format()
                                for category in Category.query.all()]

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    '''
    Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
    This endpoint returns a list of questions, number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions', methods=["GET"])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format()
                               for question in Question.query.all()]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions)
        })

    '''
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_questions(question_id):
        Question.query.filter(Query.id == question_id).delete()
        db.session.commit()
        return jsonify({
            'success': True
        })

    '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=["POST"])
    def post_question():
        new_question = Question(
            question=request.form.question,
            answer=request.form.answer,
            category=request.form.category,
            difficulty=request.form.difficulty
        )

        db.session.add(new_question)
        db.session.commit()
        return jsonify({
            'success': True
        })

    '''
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search', methods=["GET"])
    def search_questions():
        search_term = request.form.get('search_term', '')
        relevant_questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format()
                               for question in relevant_questions]

        return jsonify({
            'success': True,
            'relevant_questions': formatted_questions
        })


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

'''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

return app
