from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from api import ma, db
from api.auth import token_auth
from api.models.application.applicationModels import MemberApplication


class ApplicationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MemberApplication
        ordered = True

    id = ma.auto_field(dump_only=True)
    regNo = ma.Integer(dump_only=True)
    memberID = ma.Integer(required=True)
    membershipID = ma.Integer(required=True)
    memberSubCategoryID = ma.Integer(required=True)
    productID = ma.Integer(required=True)

    member = ma.Nested('MemberSchema', dump_only=True)
    majorProduct = ma.Nested('ProductSchema', dump_only=True)
