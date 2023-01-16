import os
import uuid

from apifairy.decorators import other_responses
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response

from api.app import db, authorize
from api.models.application.applicationModels import *
from api.models.administration.adminModels import User
from api.schemas.application.applicationSchemas import *
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas.globalSchemas import DateTimePaginationSchema
from configs.helpers.image_helper import _image_resize

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

    companyRegCert = request.files['companyRegCert']
    exportRegCert = request.files['exportRegCert']
    companyProfile = request.files['companyProfile']

    if companyRegCert | exportRegCert | companyProfile and allowed_file(companyProfile.filename) | \
            allowed_file(exportRegCert.filename) | allowed_file(companyRegCert.filename):
        file_id = str(uuid.uuid4())
        filename = file_id
        companyRegCert.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        exportRegCert.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        companyProfile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        files = [{
            "companyRegCert": companyRegCert,
            "exportRegCert": exportRegCert,
            "companyProfile": companyProfile
        }]
        app_files = ApplicationFiles(**files)
        # app_files.exportRegCert = url_for('uploaded_file', filename=filename, _external=True)
        db.session.add_all(app_files)
        db.session.commit()

    newApplication = MemberApplication(memberID=member, **data)
    db.session.add(newApplication)
    db.session.commit()
    return newApplication


@application.route('/member/applications', methods=['GET'])
@authenticate(token_auth)
@paginated_response(application_schema, order_by=MemberApplication.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def member_applications_all():
    """Retrieve all applications from a user"""
    user_id = token_auth.current_user()
    member = db.session.get(User, user_id) or abort(404)
    return member.user_applications_select()
