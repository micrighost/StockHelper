from marshmallow import Schema, fields


class UsersSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
