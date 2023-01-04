from datetime import datetime
from hashlib import md5
from time import time

import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm
from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Questionnaires(Updateable, db.Model):
    __tablename__ = 'netp_questionnaires'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    auditors = sqla_orm.relationship(
        'Auditors', back_populates='questionnaire')
    sections = sqla_orm.relationship(
        'QuestionnaireSections', back_populates='questionnaire')

    def __repr__(self):
        return '<Questionnaires {}>'.format(self.text)


class Auditors(Updateable, db.Model):
    __tablename__ = 'netp_auditors'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    title = sqla.Column(sqla.String(1000), nullable=False)
    questionnaire_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_questionnaires.id'),
                                   index=True)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    questionnaire = sqla_orm.relationship(
        'Questionnaires', back_populates='auditors')

    def __repr__(self):
        return '<Auditors {}>'.format(self.text)


class QuestionnaireSections(Updateable, db.Model):
    __tablename__ = 'netp_questionnaire_sections'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(200), nullable=False)
    section_no = sqla.Column(sqla.Integer, nullable=False)
    questionnaire_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_questionnaires.id'),
                                   index=True)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    questionnaire = sqla_orm.relationship(
        'Questionnaires', back_populates='sections')
    questions = sqla_orm.relationship(
        'Questions', back_populates='section')

    def __repr__(self):
        return '<QuestionnaireSections {}>'.format(self.text)


class Questions(Updateable, db.Model):
    __tablename__ = 'netp_questions'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(500), nullable=False)
    section_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_questionnaire_sections.id'),
                             index=True)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    section = sqla_orm.relationship(
        'QuestionnaireSections', back_populates='questions')

    def __repr__(self):
        return '<Questions {}>'.format(self.text)


class Answers(Updateable, db.Model):
    __tablename__ = 'netp_answers'

    id = sqla.Column(sqla.Integer, primary_key=True)
    answer = sqla.Column(sqla.String(100), nullable=False)
    question_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_questions.id'),
                              index=True)
    member_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_members.id'),
                            index=True)
    question = sqla_orm.relationship('Questions')
    member = sqla_orm.relationship('Members')
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Answers {}>'.format(self.text)
