from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from api.models.questionnaire.questionnaireModel import Questionnaires, QuestionnaireSections, Questions, Answers
from api.schemas.questionnaire.questionnaireSchema import QuestionnaireSchema, QuestionnaireSectionSchema, QuestionSchema, AnswerSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas.schemas import DateTimePaginationSchema

questionnaire = Blueprint('questionnaire', __name__)
questionnaire_schema = QuestionnaireSchema()
questionnaires_schema = QuestionnaireSchema(many=True)

# auditor_schema = AuditorSchema()
# auditors_schema = AuditorSchema(many=True)

section_schema = QuestionnaireSectionSchema()
sections_schema = QuestionnaireSectionSchema(many=True)

question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)


@questionnaire.route('/questionnaires/all')
@paginated_response(questionnaires_schema, order_by=Questionnaires.created_on,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all():
    """Get All Questionnaires"""
    return Questionnaires.select()


@questionnaire.route('/questionnaires', methods=['POST'])
@body(questionnaire_schema)
@response(questionnaire_schema)
def new_questionnaire(data):
    """New Questionnaire"""
    newQuestionnaire = Questionnaires(**data)
    db.session.add(newQuestionnaire)
    db.session.commit()
    return newQuestionnaire


# @questionnaire.route('/questionnaires/auditor', methods=['POST'])
# @body(auditor_schema)
# @response(auditor_schema)
# def new_auditor(data):
#     """New Auditor"""
#     newAuditor = Auditors(**data)
#     db.session.add(newAuditor)
#     db.session.commit()
#     return newAuditor


@questionnaire.route('/questionnaires/section', methods=['POST'])
@body(section_schema)
@response(section_schema)
def new_section(data):
    """New Section"""
    newSection = QuestionnaireSections(**data)
    db.session.add(newSection)
    db.session.commit()
    return newSection


@questionnaire.route('/questionnaires/question', methods=['POST'])
@body(question_schema)
@response(question_schema)
def new_question(data):
    """New Question"""
    newQuestion = Questions(**data)
    db.session.add(newQuestion)
    db.session.commit()
    return newQuestion


@questionnaire.route('/questionnaires/answer', methods=['POST'])
@body(answer_schema)
@response(answer_schema)
def new_answer(data):
    """New Answer"""
    newAnswers = Answers(**data)
    db.session.add(newAnswers)
    db.session.commit()
    return newAnswers
