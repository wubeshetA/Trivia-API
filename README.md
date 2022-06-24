# Trivia API
This project is Trivia question and answer web app. A user can select a category of question and attempt to answer them. If the user cannot answer the question they can click 'show answer' button next to each question and see the answer. If a question is not valid question or if the user do not want to see that question on the list they can delete it. In addition, the app also has a feature to add custom questions with their answers and access them on another time.

The project is built mainly to demonstrate API design and development skill. All the endpoints of the API are tested with unittest.
# Getting Started
## Installing dependencies
### Python 3.7 or later
To run this project, python3.7 or later is required. visit the official [python](https://www.python.org/) wesite to install it.
### Virtual Environment
While working on this project, we recommend using Virtual Environment.
The following steps can be followed to install and activate the virtual environment
```shell
pip install virtualenv
```
In the root directory of the project, run the following command activate the virtual environment
```shell
python -m venv env
source env/bin/activate
```
### Pip Dependencies
After setting up the virtual environment, navigate to the `/backend` directory and run the following command to install all the dependencies required.
```python
pip install -r requirements.txt
```
## Database setup
This project runs on postgresql. However you are free to use other databases such as SQLite as the code is written with SQLAlchemy ORM. Follow the following steps to configure and populate the database with sample data
- first install [postgresql](https://www.postgresql.org/)
- Then run the following command from the backend directory
```shell
psql trivia < trivia.psql
```
## Running server
From the '/backend' directory, run the following command to run the server
```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
## Running Frontend
View the [Frontend README](./frontend/README.md) to see how to run the frontend
# API Reference
## Error handling
Erros are returned as JSON object in the following format
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:

- 404: Resource Not Found 
- 400: Bad Request 
- 422: Not Processable 
- 500: Internal Server Error 
- 405: Method Not Allowed

## Endpoints
### GET /categories
- General:
    - returns all avaliable categories in the database and success
- Sample: ```curl http://127.0.0.1:5000/categories```
```json
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
### GET /questions
- General: 
    - returns a list of question objects, success, total questions, Categories
    - results are paginated in group of 10
    - Include request argument to select page number
- Sample: ```curl http://127.0.0.1:5000/questions```
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
   
  "questions": [
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
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 18,
  "current_category": "History"
}
```
### DELETE /questions/{int}
- General: 
    - Delete a question with the given id
    - return success value
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/16```
```json
{
    "success": true 
}
```
### POST /questions
- General:
    - create a question using the submitted question, answer, difficulty, category
    - return success value
    - if searchTerm is provided it returns success value, questions that much the searchTerm (case insensitive), total questions,categories
- Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is known as the father of Computer Science?", "answer": "Alan Turing","category" :"4", "difficulty":"5"}'```
```json
{
    "success": true
}
```
- When Search Term is provided
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What is"}'`
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "History", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}
```
### GET /categories/{int}/questions
- General:
    - Get questions from the given category by id.
    - Returns success value, paginated questions, total number of questions, current category
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
```json
{
  "current_category": "Science", 
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
  "total_questions": 18
}
```
### POST /quizzes
- General:
    - Get category and list of id of previous questions (if the quizzes is just starting the list can be empty list).
    - Returns next random question in the same categor, success value
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"History","id":"4"}, "previous_questions":[9]}'`
```json
{
  "question": {
    "answer": "George Washington Carver", 
    "category": 4, 
    "difficulty": 2, 
    "id": 12, 
    "question": "Who invented Peanut Butter?"
  }, 
  "success": true
}
```
# Deployment
# Authors
- Backend/API : [Wubeshet Anegagrie Yimam](https://linkedin.com/in/wubeshet)
- Frontend: Udacity team
# Acknowledgements
- To my course instructor, Kerry McCarthy
- To all student of ALX-T<->Udacity and weekly session leads 

