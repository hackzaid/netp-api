from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from api.models.questionnaire.questionnaireModel import Questionnaires, Auditors, QuestionnaireSections, Questions, Answers
from api.schemas.questionnaire.questionnaireSchema import QuestionnaireSchema, CategorySchema
from api.auth import token_auth
from api.decorators import paginated_response

questionnaire = Blueprint('questionnaire', __name__)
questionnaire_schema = QuestionnaireSchema()
questionnaires_schema = QuestionnaireSchema(many=True)


@questionnaire.route('/questionnaires/all')
@response(QuestionnaireSchema)
def get_questionnaires():
    """Get All Questionnaires"""
    return Questionnaires.select()
