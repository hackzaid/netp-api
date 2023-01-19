from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.app import db, authorize
from api.models.inspection.inspectionModels import InspectionFormSection, Question, \
    Answer, InspectionForm, Inspector, Inspection
from api.schemas.globalSchemas import DateTimePaginationSchema
from api.schemas.inspection.inspectionSchema import InspectionFormSectionSchema, QuestionSchema, \
    AnswerSchema, InspectionFormSchema, InspectorSchema, InspectionSchema
from api.auth import token_auth
from api.decorators import paginated_response, check_confirmed

inspection = Blueprint('inspection', __name__)
inspection_schema = InspectionSchema()
inspections_schema = InspectionSchema(many=True)

inspection_form_schema = InspectionFormSchema()
inspection_forms_schema = InspectionFormSchema(many=True)

inspection_form_section_schema = InspectionFormSectionSchema()
inspection_form_sections_schema = InspectionFormSectionSchema(many=True)

inspector_schema = InspectorSchema()
inspectors_schema = InspectorSchema()

question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)


@inspection.route('/inspections/member/<int:member_id>')
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@paginated_response(inspection_schema, order_by=Inspection.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all_inspections(member_id):
    """All Inspections For A Member"""
    return db.session.query(InspectionFormSection).filter(Inspection.member_id == member_id)


@inspection.route('/inspection/forms')
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@paginated_response(inspection_forms_schema, order_by=InspectionForm.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all_forms():
    """All Inspection Form"""
    return InspectionForm.select()


@inspection.route('/inspection/forms/sections/<int:form_id>')
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@paginated_response(inspection_form_sections_schema, order_by=InspectionFormSection.section_no,
                    order_direction='asc',
                    pagination_schema=DateTimePaginationSchema)
def all_form_sections(form_id):
    """All Inspection Form sections"""
    return db.session.query(InspectionFormSection).filter(InspectionFormSection.inspection_form_id == form_id)


@inspection.route('/inspection', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@body(inspection_schema)
@response(inspection_schema)
def new_inspection(data):
    """New Inspection"""
    newInspection = Inspection(**data)
    db.session.add(newInspection)
    db.session.commit()
    return newInspection


@inspection.route('/inspection/forms', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@body(inspection_form_schema)
@response(inspection_form_schema)
def new_inspection_form(data):
    """New Inspection Form"""
    newInspectionForm = InspectionForm(**data)
    db.session.add(newInspectionForm)
    db.session.commit()
    return newInspectionForm


@inspection.route('/inspection/forms/sections', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@body(inspection_form_section_schema)
@response(inspection_form_section_schema)
def new_section(data):
    """New Inspection Form Section"""
    newSection = InspectionFormSection(**data)
    db.session.add(newSection)
    db.session.commit()
    return newSection


@inspection.route('/inspection/inspectors', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@body(inspector_schema)
@response(inspector_schema)
def new_inspector(data):
    """New Inspector"""
    newInspector = Inspector(**data)
    db.session.add(newInspector)
    db.session.commit()
    return newInspector


@inspection.route('/inspection/forms/question', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@body(questions_schema)
@response(questions_schema)
def new_question(data):
    """New Question"""
    newQuestions = []
    for question in data:
        newQuestions.append(Question(**question))

    db.session.add_all(newQuestions)
    db.session.commit()
    return newQuestions


@inspection.route('/inspection/answers', methods=['POST'])
@authenticate(token_auth)
@check_confirmed
@authorize.has_role('admin')
@body(answers_schema)
@response(answers_schema)
def new_answer(data):
    """New Answer"""
    newAnswers = []
    for answer in data:
        newAnswers.append(Answer(**answer))

    db.session.add_all(newAnswers)
    db.session.commit()
    return newAnswers
