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
from api.decorators import paginated_response, check_confirmed
from api.schemas.globalSchemas import DateTimePaginationSchema

application = Blueprint('application', __name__)
application_schema = ApplicationSchema()

ALLOWED_EXTENSIONS = set(['pdf', 'doc'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/application/<int:regNo>', methods=['GET'])
@authenticate(token_auth)
@check_confirmed
@authorize.read
@response(application_schema)
def get_application(regNo):
    """Get Member Application"""
    return MemberApplication.select()


@application.route('/application', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@body(application_schema, location="form")
@response(application_schema)
def new_application(data):
    """New Application for Member
    This endpoint will assume the member has already registered on the platform and all actions will have his/her
    user ID attached to it.
    """
    global newApplication

    member_id = token_auth.current_user()
    # encryptUUID = uuid.SafeUUID
    # print(encryptUUID)
    # Get Application Data
    application_data = [{
        "productID": data['productID'],
        "businessType": data['businessType'],
        "companyDescription": data['companyDescription'],
        "exportNo": data['exportNo']
    }]

    for appData in application_data:
        newApplication = MemberApplication(member=member_id, **appData)
        newApplication.regNo = datetime.strftime(datetime.utcnow(), "%y%m%d%H%M%S")
        db.session.add(newApplication)
        db.session.flush()

    companyRegCert = request.files['companyRegCert']
    exportRegCert = request.files['exportRegCert']
    companyProfile = request.files['companyProfile']

    if companyRegCert or exportRegCert or companyProfile and allowed_file(companyProfile.filename2) or \
            allowed_file(exportRegCert.filename2) or allowed_file(companyRegCert.filename1):

        filename1 = str(uuid.uuid4())
        filename2 = str(uuid.uuid4())
        filename3 = str(uuid.uuid4())

        companyRegCert.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename1))
        exportRegCert.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename2))
        companyProfile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename3))

        files = [{
            "companyRegCert": companyRegCert,
            "exportRegCert": exportRegCert,
            "companyProfile": companyProfile
        }]
        for app_file in files:
            app_files = ApplicationFiles(**app_file)
            app_files.applicationID = newApplication.id
            app_files.exportRegCert = url_for('uploaded_file', filename=filename2, _external=True)
            app_files.companyRegCert = url_for('uploaded_file', filename=filename1, _external=True)
            app_files.companyProfile = url_for('uploaded_file', filename=filename3, _external=True)
            db.session.add(app_files)
        db.session.commit()
        db.session.close()
    return newApplication


@application.route('/member/applications', methods=['GET'])
@authenticate(token_auth)
@check_confirmed
@response(application_schema)
@other_responses({404: 'User not found'})
def member_applications_all():
    """Retrieve all applications for member"""
    user_id = token_auth.current_user()
    member = db.session.get(MemberApplication, 20) or abort(404)
    print(user_id)
    return member
