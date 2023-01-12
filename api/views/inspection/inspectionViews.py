from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from api.models.inspection.inspectionModels import InspectionFormSection, Question, \
    Answer, InspectionForm, Inspector, Inspection
from api.schemas.inspection.inspectionSchema import InspectionFormSectionSchema, QuestionSchema, \
    AnswerSchema, InspectionFormSchema, InspectorSchema, InspectionSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas.schemas import DateTimePaginationSchema

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
@paginated_response(inspection_schema, order_by=Inspection.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all(member_id):
    """Get All Inspections For A Member"""
    return Inspection.query.filter(Inspection.member_id == member_id).all()


@inspection.route('/inspection/forms')
@paginated_response(inspection_forms_schema, order_by=InspectionForm.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all_forms():
    """Get All Inspection Form"""
    return InspectionForm.select()


@inspection.route('/inspection', methods=['POST'])
@body(inspection_schema)
@response(inspection_schema)
def new_inspection(data):
    """New Inspection"""
    newInspection = Inspection(**data)
    db.session.add(newInspection)
    db.session.commit()
    return newInspection


@inspection.route('/inspection/forms', methods=['POST'])
@body(inspection_form_schema)
@response(inspection_form_schema)
def new_inspection_form(data):
    """New Inspection Form"""
    newInspectionForm = InspectionForm(**data)
    db.session.add(newInspectionForm)
    db.session.commit()
    return newInspectionForm


@inspection.route('/inspection/forms/sections', methods=['POST'])
@body(inspection_form_section_schema)
@response(inspection_form_section_schema)
def new_section(data):
    """New Inspection Form Section"""
    newSection = InspectionFormSection(**data)
    db.session.add(newSection)
    db.session.commit()
    return newSection


@inspection.route('/inspection/inspectors', methods=['POST'])
@body(inspector_schema)
@response(inspector_schema)
def new_inspector(data):
    """New Inspector"""
    newInspector = Inspector(**data)
    db.session.add(newInspector)
    db.session.commit()
    return newInspector


@inspection.route('/inspection/forms/question', methods=['POST'])
@body(question_schema)
@response(question_schema)
def new_question(data):
    """New Question"""
    newQuestion = Question(**data)
    db.session.add(newQuestion)
    db.session.commit()
    return newQuestion


@inspection.route('/inspection/answers', methods=['POST'])
@body(answer_schema)
@response(answer_schema)
def new_answer(data):
    """New Answer"""
    newAnswers = Answer(**data)
    db.session.add(newAnswers)
    db.session.commit()
    return newAnswers
