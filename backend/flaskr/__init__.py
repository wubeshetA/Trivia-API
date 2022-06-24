from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sympy import Q, re

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# paginate questions based on the given page number
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins.
    """
    CORS(app, resources={
        "/*" : {
            "origins": "*"
        }
    })

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    An endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def categories():
        
        categories = Category.query.order_by(Category.id).all()    
        formated_category = {category.id: category.type for category in categories}
        # for category in categories:
        #     formated_category[category.id] = category.type
        
        return jsonify(
            {
                "success": True,
                "categories": formated_category
            }
        )


    """

    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():

        all_questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_questions(request, all_questions)

        categories = Category.query.order_by(Category.id).all()    
        formated_category = {category.id: category.type for category in categories}

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": paginated_questions,
                "total_questions":len(Question.query.all()),
                "categories":formated_category,
                "current_category":"History"
            }
        )

    """
    
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:

            question = Question.query.filter(Question.id == id).one_or_none()
            if question == None:
                abort(404)
            question.delete()
            return jsonify(
                {
                    "success": True
                }
            )
        except:
            abort(422)
    

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():

        try:
            body = request.get_json()
            question = body.get('question')
            answer = body.get('answer')
            difficulty = body.get('difficulty')
            category = body.get('category')
            
            search_term = body.get('searchTerm')
            if search_term:
                selection = (Question.query.order_by(Question.id)
                .filter(Question.question.ilike("%{}%".format(search_term))))
                paginated_questions = paginate_questions(request, selection)
                

                categories = Category.query.order_by(Category.id).all()    
                formated_category = {category.id: category.type for category in categories}

                return jsonify(
                    {
                        "success": True,
                        "questions": paginated_questions,
                        "total_questions":len(Question.query.all()),
                        "categories":formated_category,
                        "current_category":"History"
                    }
                )


            else:
                new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                new_question.insert()

                return jsonify(
                {
                    "success": True
                }
                ) 
            
        except:
            abort(422)



    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:id>/questions")
    def get_questions_for_category(id):

        selection = Question.query.filter(Question.category == id).all()
        paginated_questions = paginate_questions(request, selection)
        category = Category.query.get(id)

        return jsonify(
            {
              "success": True,
              "questions": paginated_questions,  
              "total_questions": len(Question.query.all()),
              "current_category": category.type
            }
        )

    """
 
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def quizzes():

        body = request.get_json()
        
        # check if the user select 'All' questions or from category
        # it query questions which their id is not found in previous_questions
        # 'All' has an id of '0'
        try:
            # check if the the parameters are valid and provided
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            if quiz_category['id'] == 0:
                avaliable_questions = (Question.query
                .filter(Question.id.notin_(previous_questions))
                .all())
            # if user select category
            else:
                avaliable_questions = (Question.query.order_by(Question.id)
                .filter(Question.category == quiz_category['id'])
                .filter(Question.id.notin_(previous_questions)).all())

            # if the user play all the avaliable questions
            # and there are no more questions
            if len(avaliable_questions) == 0:
                print("================here I am empty================ ")
                return jsonify(
                    {
                        "question": False,
                    }
                )
            
            # if there are avalible questions choose random one question from them
            next_question = random.choice(avaliable_questions)

            # return the choosen random question
            return jsonify (
                {
                    "success": True,
                    "question": next_question.format()
                }
            )
        except:
            abort (422)

    """
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False,
            "error": 422,
            "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {"success": False,
            "error": 400,
            "message": "bad request"
            }
            ), 400
    @app.errorhandler(500)
    def server_error(error):
        return jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error"
            }
        )
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
                }
        )

    return app

