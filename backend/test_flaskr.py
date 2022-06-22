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


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('student', 'student','localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test GET request for /categories route
    def test_get_all_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # def test_404_get_no_categories(self):
    #     res = self.client().get("/categories")
    #     data = json.loads("{}")

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "resource not found")

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
    # =============== UNCOMMNET THE FOLLOWING TEST====================

    # def test_delete_question(self):
    #     res=self.client().delete('/questions/22')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
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

    # test POST request to add new question fails
    # def test_422_if_add_question_fails(self):
    #     res = self.client().post('/questions', json = self.new_question)
    #     data = json.loads(res.data)
    #     pass

    # test POST request for searching questions
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



        
        


    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()