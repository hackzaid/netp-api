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


@application.route('/application', methods=['GET'])
@response(application_schema)
def get_application():
    """Get Member Application"""
    return MemberApplication.select()
