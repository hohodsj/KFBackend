from marshmallow import Schema, fields

class ProfileSchema(Schema):
    name = fields.Str()
    about = fields.Str()


class QNASchema(Schema):
    id = fields.Int(required=True)
    question = fields.Str(required=True)
    answer = fields.Str()
    hint = fields.Str()
