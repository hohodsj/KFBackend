from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import QNASchema
from db import db
from models import QnaModel

blp = Blueprint("QNA", __name__, description="QuestionAndAnswers")

@blp.route("/questions")
class Questions(MethodView):
    @blp.response(200, QNASchema(many=True))
    def get(self):
        return QnaModel.query.with_entities(QnaModel.id, QnaModel.question, QnaModel.hint)
    
    @blp.arguments(QNASchema)
    def post(self, qna_data):
        if "id" in qna_data:
            qna_obj = QnaModel.query.get(qna_data["id"])
            if qna_obj and qna_data["answer"] == qna_obj.answer:
                return {'verified':True}
            elif qna_obj and qna_data["answer"] != qna_obj.answer:
                print(f'Input {qna_data["answer"]} is not {qna_obj.answer}')
            else:
                print(f'{qna_data=} does not exists in db')
        else:
            print(f'{qna_data=} id field is missing')
        return {'verified': False}

@blp.route("/questions-answers")
class QuestionsAnswers(MethodView):
    @blp.response(200, QNASchema(many=True))
    def get(self):
        return QnaModel.query.all()
    
    @blp.arguments(QNASchema)
    @blp.response(201, QNASchema)
    def post(self, qna_data):
        print(f'upsert: {qna_data=}')
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
    @blp.response(201, QNASchema)
    def put(self, qna_data):
        print(f'put(update) {qna_data=}')
        qna = QnaModel.query.get(qna_data.id)
        if qna:
            qna.question = qna_data["question"]
            qna.answer = qna_data["answer"]
            qna.hint = qna_data["hint"]

    