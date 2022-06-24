from cgitb import reset
from dataclasses import dataclass
import dataclasses
from hashlib import new
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from requests import request

from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_user = DB_USER
        self.database_passwd = DB_PASSWORD
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_user, self.database_passwd,'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "what is the country that is  known as 'the land of origins'?",
            "answer": "Ethiopia",
            "difficulty": 4,
            "category": 4
            }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # test GET request for /categories route
    def test_get_all_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

   
    # test Get request for getting paginated questions
    def test_get_paginated_questions(self):
        res= self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
    
    # test Get request for getting questions beyond the valid page limit
    def test_404_sent_requesting_beyond_valid_page(self):
        res=self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # test DELETE request ot delete a question with id
    def test_delete_question(self):
        res=self.client().delete('/questions/20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # test DELETE  request if deletion fails
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test POST request for adding a new question
    def test_add_question(self):
        res = self.client().post('/questions', json = self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    # test POST request for searchTerm
    def test_search_questions(self):
        res = self.client().post('/questions', json = {"searchTerm": "what is"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 

    # test POST request for search with out result
    def test_search_questions_without_result(self):
        res = self.client().post('/questions', json = {"searchTerm": "This is random search term"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test GET request to get questions only from a particular category
    def test_get_questions_from_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
    
    # test POST request for quizzes
    def test_quizzes(self):

        res = self.client().post('/quizzes', json = {'previous_questions':[], 'quiz_category': {'type': 'Science', 'id': '1'}})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test POST request of quizzes with wrong parameters
    def test_404_quizzes(self):
        res = self.client().post('/quizzes', json={'wrong_previous_questions':[],'wrong_quiz_category': {'type': 'Engineering', 'id': 7}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()