# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute (on Windows replace `export` by `set`):

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:

```JSON
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
* `400`: Bad Request
* `404`: Resource Not Found
* `405`: Method not allowed
* `422`: Not Processable

### Endpoint Library
#### GET /categories
* General:
  * Returns a dictionary of category objects and success value
* Sample: `curl -X GET http://127.0.0.1:5000/categories`

```JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions
* General:
  * Returns a list of question objects, success value, total number of questions, categories and current category (currently unused). 
  * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
* Sample: `curl -X GET http://127.0.0.1:5000/questions`

```JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### DELETE /questions/{question_id}
* General:
  * Deletes the question of the given ID if it exists. Returns the id of the deleted question and the success value.
* Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`

```JSON
{
  "deleted": 2,
  "success": true
}
```


#### POST /questions
* General:
  * Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question and the success value.
* Sample: `curl http://127.0.0.1:5000/questions -X POST  -H "Content-Type: application/json" -d '{"question":"What is the highest mountain in Germany?", "answer":"Zugspitze", "category":"3", "difficulty":"2"}'`
* Sample (Windows): `curl http://127.0.0.1:5000/questions -X POST  -H "Content-Type: application/json" -d "{\"question\":\"What is the highest mountain in Germany?\", \"answer\":\"Zugspitze\", \"category\":\"3\", \"difficulty\":\"2\"}"`

```JSON
{
  "created": 26,
  "success": true
}
```

#### POST /questions_search
* General:
  * Searches questions based on provided search term. Returns a list of question objects containing the search term, the total number of questions containing the search term and the success value.
* Sample: `curl http://127.0.0.1:5000/questions_search -X POST  -H "Content-Type: application/json" -d '{"search_term":"title"}'`
* Sample (Windows): `curl http://127.0.0.1:5000/questions_search -X POST  -H "Content-Type: application/json" -d "{\"searchTerm\":\"title\"}"`

```JSON
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### GET /categories/{category_id}/questions
* General:
  * Based on a given category id this will return a list of all question objects in the category.
* Sample: `curl -X GET http://127.0.0.1:5000/categories/1/questions`

```JSON
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### POST /quizzes
* General:
  * Based on the current category and the previously asked questions, this request will return the next question to answer. 
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST  -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Science", "id":1}}'`
* Sample (Windows): `curl http://127.0.0.1:5000/quizzes -X POST  -H "Content-Type: application/json" -d "{\"previous_questions\":[], \"quiz_category\":{\"type\":\"Science\", \"id\":1}}"`

```JSON
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```
