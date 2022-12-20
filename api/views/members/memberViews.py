from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.app import db, authorize
from api.models.membership.memberModel import Members, ContactPersons, MemberType
from api.schemas.membership.memberSchema import MemberSchema, ContactPersonSchema, MembershipTypeSchema
from api.auth import token_auth
from api.decorators import paginated_response

members = Blueprint('members', __name__)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

membership_type_schema = MembershipTypeSchema()
membership_types_schema = MembershipTypeSchema(many=True)


@members.route('members/all/', methods=['GET'])
@authenticate(token_auth)
@response(member_schema)
def get_all_members():
    """Retrieve All Members"""
    return Members.select()


@members.route('/member/type', methods=['POST'])
@authenticate(token_auth)
@body(membership_type_schema)
@response(membership_type_schema)
def membership_type_add(args):
    """Add Membership Type"""
    membership = MemberType(**args)
    db.session.add(membership)
    db.session.commit()
    return membership


@members.route('member/add', methods=['POST'])
@response(member_schema)
@body(member_schema)
def add_member(args):
    """Member Onboarding"""
    member = Members(**args)
    member.regNo = 299930
    db.session.add(member)
    db.session.commit()
    return
