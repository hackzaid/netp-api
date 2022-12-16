from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from api import ma, db
from api.auth import token_auth
from api.models.membership.memberModel import Members, ContactPersons


class MemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Members
        ordered = True

    id = ma.auto_field(dump_only=True)
    regNo = ma.Integer(dump_only=True)
    firstName = ma.String(required=True, validate=validate.Length(min=3, max=64))
    lastName = ma.String(required=True, validate=validate.Length(min=3, max=64))
    village = ma.String(required=True, validate=validate.Length(min=3, max=64))
    region = ma.String(required=True, validate=validate.Length(min=3, max=64))

    contactPersons = ma.Nested('ContactPersonSchema', many=True, dump_only=True)


class ContactPersonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ContactPersons
        ordered = True

    id = ma.auto_field(dump_only=True)
    c_firstName = ma.String(required=True, validate=validate.Length(min=3, max=64))
    c_lastName = ma.String(required=True, validate=validate.Length(min=3, max=64))
    c_position = ma.String(required=True, validate=validate.Length(min=3, max=64))
    c_phone = ma.String(required=True, validate=validate.Length(min=3, max=64))
    c_workphone = ma.String(required=True, validate=validate.Length(min=3, max=64))
    c_email = ma.String(required=True, validate=validate.Length(min=3, max=64))
    c_memberID = ma.Integer(required=True)
