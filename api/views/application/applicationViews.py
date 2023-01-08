from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.app import db, authorize
from api.models.application.applicationModels import *
from api.schemas.application.applicationSchemas import *
from api.auth import token_auth
from api.decorators import paginated_response

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
@body(application_schema, location='form')
@response(application_schema)
def new_application(data):
    """New Application for Member"""
    newApplication = MemberApplication(**data)
    db.session.add(newApplication)
    db.session.commit()
    return newApplication
