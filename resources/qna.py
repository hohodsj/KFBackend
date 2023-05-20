from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import QNASchema
from db import db
from models import QnaModel
import requests
import os

blp = Blueprint("QNA", __name__, description="QuestionAndAnswers")

def send_email(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    api = os.getenv("MAILGUN_API_KEY")
    print(f'domain:{domain}  api:{api} subject:{subject} body:{body}')
    requests.post(
        f'https://api.mailgun.net/v3/{domain}/messages',
        auth=("api", api),
        data={"from": 'Excited User <mailgun@{domain}>',
            "to": [to],
            "subject": subject,
            "text": body})
    
    

@blp.route("/questions")
class Questions(MethodView):
    @blp.response(200, QNASchema(many=True))
    def get(self):
        return QnaModel.query.order_by(QnaModel.id).with_entities(QnaModel.id, QnaModel.question, QnaModel.hint).order_by(QnaModel.id)
    
    @blp.arguments(QNASchema)
    def post(self, qna_data):
        to = []
        user1_email = os.getenv("USER1_EMAIL")
        print(user1_email)
        if user1_email:
            to.append(user1_email)
        if os.getenv("USER2_EMAIL"):
            to.append(os.getenv("USER2_EMAIL"))
        if "id" in qna_data:
            qna_obj = QnaModel.query.get(qna_data["id"])
            if qna_obj and qna_data["answer"].lower().replace(" ","") == qna_obj.answer.lower().replace(" ",""):
                subject = f'Question {qna_obj.id} PASS'
                body = f'Kathleen answer {qna_data["answer"]} match actual answer {qna_obj.answer}'
                send_email(to, subject, body)
                return {'verified':True}
            elif qna_obj and qna_data["answer"] != qna_obj.answer:
                subject = f'Question {qna_obj.id} FAIL'
                body = f'Kathleen answer {qna_data["answer"]} NOT match actual answer {qna_obj.answer}'
                send_email(to, subject, body)
                print(f'Input {qna_data["answer"]} is not {qna_obj.answer}')
            else:
                print(f'{qna_data} does not exists in db')
        else:
            print(f'{qna_data} id field is missing')
        return {'verified': False}

@blp.route("/questions-answers")
class QuestionsAnswers(MethodView):
    @blp.response(200, QNASchema(many=True))
    def get(self):
        return QnaModel.query.order_by(QnaModel.id).all()
    
    @blp.arguments(QNASchema)
    @blp.response(201, QNASchema)
    def post(self, qna_data):
        qna_obj = QnaModel.query.get(qna_data["id"]) if "id" in qna_data else QnaModel(**qna_data)
        if qna_obj:
            print('update')
            qna_obj.question = qna_data["question"]
            qna_obj.answer = qna_data["answer"]
            qna_obj.hint = qna_data["hint"]
        try:
            db.session.add(qna_obj)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="IntegrityError: {e}")
        except SQLAlchemyError as e:
            abort(500, message="SQLAlchemyError: {e}")
        return qna_obj
    
    @blp.arguments(QNASchema)
    @blp.response(201)
    def delete(self, qna_data):
        qna_obj = QnaModel.query.get_or_404(qna_data["id"])
        try:
            db.session.delete(qna_obj)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="IntegrityError: {e}")
        except SQLAlchemyError as e:
            abort(500, message="SQLAlchemyError: {e}")
        return {'delete': True}

    