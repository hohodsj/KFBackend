from marshmallow import Schema, fields

class ProfileSchema(Schema):
    name = fields.Str()
    about = fields.Str()

class QuestionHint(Schema): # UI
    id = fields.Int()
    question = fields.Str(required=True)
    hint = fields.Str()

class QNASchema(QuestionHint): # Admin
    answer = fields.Str()

