from marshmallow import Schema, validate, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=64)])
    email = fields.String(required=True, validate=[validate.Length(max=120)])
    password_hash = fields.String(required=True, validate=[validate.Length(max=128)], load_only=True)
    poster = fields.String(required=True)


class VideoSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(max=100)])
    slug = fields.String(required=True, validate=[validate.Length(max=150)])
    genres_id = fields.Integer(dump_only=True)
    release_date = fields.DateTime(dump_only=True)
    producer_id = fields.Integer(dump_only=True)
    body = fields.String(required=True, validate=[validate.Length(max=500)])
    poster = fields.String(required=True)
    user_id = fields.Integer(dump_only=True)
    publication = fields.DateTime(dump_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
