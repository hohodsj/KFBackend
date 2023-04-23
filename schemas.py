from marshmallow import Schema, fields

class ProfileSchema(Schema):
    name = fields.Str()
    about = fields.Str()