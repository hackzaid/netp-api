from apifairy.decorators import other_responses
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response

from api.app import db, authorize
from api.models.membership.memberModel import Members, ContactPersons, MemberType, MemberSubCategory
from api.schemas.membership.memberSchema import MemberSchema, ContactPersonSchema, MembershipTypeSchema, \
    MembershipSubCategorySchema
from api.auth import token_auth, basic_auth
from api.decorators import paginated_response

members = Blueprint('members', __name__)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

membership_type_schema = MembershipTypeSchema()
membership_types_schema = MembershipTypeSchema(many=True)

membership_sub_cat_Schema = MembershipSubCategorySchema()



@members.route('members/all/', methods=['GET'])
@authenticate(token_auth, role=['admin'])
@paginated_response(member_schema)
def get_all_members():
    """Retrieve All Members"""
    print(request.environ.get('HTTP_AUTHORIZATION'))
    return Members.select()


@members.route('/member/type', methods=['POST'])
@authenticate(token_auth)
@authorize.read
@body(membership_type_schema)
@response(membership_type_schema)
def membership_type_add(args):
    """Add Membership Type"""
    membership = MemberType(**args)
    db.session.add(membership)
    db.session.commit()
    return membership


@members.route('member/add', methods=['POST'])
@authenticate(token_auth)
@authorize.create(Members)
@response(member_schema)
@body(member_schema)
def add_member(args):
    """Member Onboarding"""
    member = Members(**args)
    member.regNo = 299930
    db.session.add(member)
    db.session.commit()
    return


@members.route('membershiptype/all/', methods=['GET'])
@authenticate(token_auth)
@paginated_response(membership_type_schema)
def get_all_membershiptype():
    """Retrieve Membership Types"""
    return MemberType.select()


@members.route('membership/subcategory/all/', methods=['GET'])
@authenticate(token_auth)
@paginated_response(membership_sub_cat_Schema)
def get_all_member_sub_cat():
    """Retrieve Membership Sub Categories"""
    return MemberSubCategory.select()


@members.route('/membership/subcategory/', methods=['POST'])
@authenticate(token_auth)
@body(membership_sub_cat_Schema)
@response(membership_type_schema)
def membership_sub_cat(args):
    """Add Membership Sub Category"""
    membershipSubCat = MemberSubCategory(**args)
    db.session.add(membershipSubCat)
    db.session.commit()
    return membershipSubCat
