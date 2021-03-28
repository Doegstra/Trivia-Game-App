# Full Stack API Project

## Full Stack Trivia

This is a trivia app to see who's the most knowledgeable person. The application can:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## READMEs
The READMEs are found in:
1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

## About the Stack

### Backend

The `./backend` directory contains a Flask and SQLAlchemy server. The main file is app.py where endpoints are defined and models.py is referenced for the DB and SQLAlchemy setup.

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. The frontend was already set up by Udacity. 
[View the README.md within ./frontend for more details.](./frontend/README.md)
