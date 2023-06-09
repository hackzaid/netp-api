from datetime import datetime

import sqlalchemy as sqla
from flask_authorize import PermissionsMixin
from sqlalchemy import orm as sqla_orm

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class InspectionForm(Updateable, db.Model, PermissionsMixin):
    __tablename__ = 'netp_inspection_forms'
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    additional_details = sqla.Column(sqla.String(1000), nullable=True)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    form_questions = sqla_orm.relationship('Question', back_populates='inspection_form', lazy='noload')
    inspection_form_sections = sqla_orm.relationship(
        'InspectionFormSection', back_populates='inspection_form')

    def __repr__(self):
        return '<InspectionForm {}>'.format(self.text)


class InspectionFormSection(Updateable, db.Model, PermissionsMixin):
    __tablename__ = 'netp_inspection_form_sections'
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(200), nullable=False)
    section_no = sqla.Column(sqla.Integer, nullable=False)
    inspection_form_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_inspection_forms.id'),
                                     index=True)

    inspection_form = sqla_orm.relationship(
        'InspectionForm', back_populates='inspection_form_sections')
    questions = sqla_orm.relationship(
        'Question', back_populates='inspection_form_section')

    def __repr__(self):
        return '<InspectionFormSection {}>'.format(self.text)


class Question(Updateable, db.Model, PermissionsMixin):
    __tablename__ = 'netp_questions'
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(500), nullable=False)
    form_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_inspection_forms.id'), index=True)
    section_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_inspection_form_sections.id'),
                             index=True)

    inspection_form = sqla_orm.relationship(InspectionForm, back_populates='form_questions')
    inspection_form_section = sqla_orm.relationship(
        'InspectionFormSection', back_populates='questions')

    def __repr__(self):
        return '<Question {}>'.format(self.text)


class Inspector(Updateable, db.Model, PermissionsMixin):
    __tablename__ = 'netp_inspectors'
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    title = sqla.Column(sqla.String(100), nullable=False)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Inspector {}>'.format(self.text)


inspectionInspector = sqla.Table(
    'netp_inspection_inspectors',
    db.Model.metadata,
    sqla.Column('inspector_id', sqla.Integer,
                sqla.ForeignKey('netp_inspectors.id')),
    sqla.Column('inspection_id', sqla.Integer,
                sqla.ForeignKey('netp_inspections.id'))
)


class Inspection(Updateable, db.Model, PermissionsMixin):
    __tablename__ = 'netp_inspections'
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    inspection_form_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_inspection_forms.id'),
                                     index=True)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'), index=True)

    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    inspection_inspectors = sqla_orm.relationship("Inspector", secondary=inspectionInspector,
                                                  backref='netp_inspections')
    user = sqla_orm.relationship('User', foreign_keys="[Inspection.user_id]")
    owner = sqla_orm.relationship("User", foreign_keys="[Inspection.owner_id]", overlaps="user")

    inspection_form = sqla_orm.relationship('InspectionForm')
    answers = sqla_orm.relationship('Answer', back_populates='inspection')

    def __repr__(self):
        return '<Inspections {}>'.format(self.text)


class Answer(Updateable, db.Model, PermissionsMixin):
    __tablename__ = 'netp_answers'
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    answer = sqla.Column(sqla.String(100), nullable=False)
    question_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_questions.id'),
                              index=True)
    question = sqla_orm.relationship('Question')
    inspection_id = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_inspections.id'),
                                index=True)
    inspection = sqla_orm.relationship('Inspection', back_populates='answers')

    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Answers {}>'.format(self.text)
