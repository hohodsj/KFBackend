from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import QNASchema

blp = Blueprint("QNA", __name__, description="QuestionAndAnswers")

@blp.route("/questions")
class Questions(MethodView):
    def get(self):
        questions = ["Question 1", "Question 2"]
        return questions

@blp.route("/questions-answers")
class QuestionsAnswers(MethodView):
    def get(self):
        qna1 = {
            "id" : 0,
            "question": "question 0",
            "answer": "answer 0",
            "hint" : "hint 0"
        }
        qna2 = {
            "id" : 1,
            "question": "question 1",
            "answer": "answer 1",
            "hint" : "hint 1"
        }
        question_answers = {"questionAnswers": [qna1, qna2]}
        return question_answers