from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from api import ma, db
from api.auth import token_auth
from api.models.questionnaire.questionnaireModel import Questionnaires, Auditors, QuestionnaireSections, Questions, Answers


class QuestionnaireSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Questionnaires
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=100))

    auditors = ma.Nested(
        'AuditorSchema', many=True, dump_only=True)

    sections = ma.Nested(
        'QuestionnaireSectionSchema', many=True, dump_only=True)


class AuditorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Auditors
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=100))
    title = ma.String(
        required=True, validate=validate.Length(min=3, max=1000))
    questionnaire_id = ma.Integer(required=True)


class QuestionnaireSectionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuestionnaireSections
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=200))
    section_no = ma.Integer(required=True)
    questionnaire_id = ma.Integer(required=True)
    questions = ma.Nested(
        'QuestionSchema', many=True, dump_only=True)


class QuestionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Questions
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.String(
        required=True, validate=validate.Length(min=3, max=500))
    section_id = ma.Integer(required=True)


class AnswerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Answers
        ordered = True

    id = ma.auto_field(dump_only=True)
    answer = ma.String(
        required=True, validate=validate.Length(min=3, max=100))
    question_id = ma.Integer(required=True)
    member_id = ma.Integer(required=True)
