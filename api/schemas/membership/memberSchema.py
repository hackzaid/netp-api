from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from api import ma, db
from api.auth import token_auth
from api.models.membership.memberModel import *


class MemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Members
        ordered = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    regNo = ma.Integer(dump_only=True)
    firstName = ma.String(required=True)
    lastName = ma.String(required=True)
    village = ma.String(required=True)
    region = ma.String(required=True)
    membershipTypeID = ma.Integer(required=True)
    membershipSubCatID = ma.Integer(required=False)

    contactPersons = ma.Nested(
        'ContactPersonSchema', many=True, dump_only=True)
    membershipType = ma.Nested('MembershipTypeSchema',  dump_only=True)


class MembershipTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MemberType
        ordered = True

    id = ma.auto_field(dump_only=True)
    title = ma.String(required=True)
    subCategory = ma.Nested('MembershipSubCategorySchema',
                            many=True, dump_only=True)


class MembershipSubCategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = MemberSubCategory
        ordered = True

    id = ma.auto_field(dump_only=True)
    title = ma.String(required=True)
    typeID = ma.Integer(required=True)


class ContactPersonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ContactPersons
        ordered = True

    id = ma.auto_field(dump_only=True)
    c_firstName = ma.String(required=True)
    c_lastName = ma.String(required=True)
    c_position = ma.String(required=True)
    c_phone = ma.String(required=True)
    c_workphone = ma.String(required=True)
    c_email = ma.String(required=True)
    c_memberID = ma.Integer(required=True)
