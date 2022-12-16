from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from api.models.membership.memberModel import Members, ContactPersons
from api.schemas.membership.memberSchema import MemberSchema, ContactPersonSchema
from api.auth import token_auth
from api.decorators import paginated_response

members = Blueprint('members', __name__)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


@members.route('allmembers/', methods=['GET'])
@response(member_schema)
def get_all_members():
    """Get All Members"""
    return Members.select()
