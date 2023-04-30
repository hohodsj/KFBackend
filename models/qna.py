from db import db

class QnaModel(db.Model):
    __tablename__ = "qna"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    hint = db.Column(db.String)
