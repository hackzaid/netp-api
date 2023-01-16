from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.app import db, authorize
from api.models.application.applicationModels import *
from api.models.administration.adminModels import User
from api.schemas.application.applicationSchemas import *
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas.globalSchemas import DateTimePaginationSchema

application = Blueprint('application', __name__)
application_schema = ApplicationSchema()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf', 'doc'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/application/<int:regNo>', methods=['GET'])
@response(application_schema)
def get_application(regNo):
    """Get Member Application"""
    return MemberApplication.select()


@application.route('/application', methods=['POST'])
@authenticate(token_auth)
@body(application_schema)
@response(application_schema)
def new_application(data):
    """New Application for Member
    This endpoint will assume the member has already registered on the platform and all actions will have his/her
    user ID attached to it.
    """
    member = token_auth.current_user()
    newApplication = MemberApplication(memberID=member, **data)
    db.session.add(newApplication)
    db.session.commit()
    return newApplication

@application.route('/users/<int:id>/applicationss', methods=['GET'])
@authenticate(token_auth)
@paginated_response(application_schema, order_by=MemberApplication.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Retrieve all applications from a user"""
    member = db.session.get(User, id) or abort(404)
    return member.user_applications_select()
