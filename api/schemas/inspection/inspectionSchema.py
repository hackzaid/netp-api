from marshmallow import validate
from api import ma, db
from api.auth import token_auth
from api.models.inspection.inspectionModels import InspectionForm, InspectionFormSection, Question, Inspector, Inspection, Answer


class InspectionFormSectionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = InspectionFormSection
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=200))
    section_no = ma.Integer(required=True)
    inspection_form_id = ma.Integer(required=True)
    questions = ma.Nested(
        'QuestionSchema', many=True, dump_only=True)


class InspectionFormSchema(ma.SQLAlchemySchema):
    class Meta:
        model = InspectionForm
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=100))
    additional_details = ma.String(
        required=True, validate=validate.Length(min=3, max=1000))
    created_on = ma.auto_field(dump_only=True)
    updated_on = ma.auto_field(dump_only=True)
    form_sections = ma.Nested(
        'InspectionFormSectionSchema', many=True, dump_only=True)


class QuestionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Question
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=500))
    inspection_form_sections_id = ma.Integer(required=True)


class InspectorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inspector
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=100))
    title = ma.String(
        required=True, validate=validate.Length(min=3, max=1000))
    created_on = ma.auto_field(dump_only=True)
    updated_on = ma.auto_field(dump_only=True)


class InspectionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inspection
        ordered = True

    id = ma.auto_field(dump_only=True)
    inspection_form_id = ma.Integer(required=True)
    member_id = ma.Integer(required=True)
    created_on = ma.auto_field(dump_only=True)
    updated_on = ma.auto_field(dump_only=True)
    inspection_inspectors = ma.Nested(
        'InspectorSchema', many=True, dump_only=True)
    member = ma.Nested('MemberSchema', dump_only=True)
    inspection_form = ma.Nested('InspectionFormSchema', dump_only=True)
    answers = ma.Nested('AnswerSchema', many=True, dump_only=True)


class AnswerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Answer
        ordered = True

    id = ma.auto_field(dump_only=True)
    answer = ma.String(
        required=True, validate=validate.Length(min=1, max=100))
    question_id = ma.Integer(required=True)
    inspection_id = ma.Integer(required=True)
