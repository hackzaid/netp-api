from datetime import datetime, timedelta
from hashlib import md5
import secrets
from time import time

from flask import current_app, url_for
import jwt
import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_authorize import PermissionsMixin
from api.models.application.applicationModels import MemberApplication

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Members(db.Model, Updateable, PermissionsMixin):
    __tablename__ = 'netp_members'
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],  # owners can revoke
        group=['read', 'update', 'revoke'],  # group can revoke
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    regNo = sqla.Column(sqla.BigInteger, unique=True, nullable=False)
    firstName = sqla.Column(sqla.String(100), nullable=False)
    lastName = sqla.Column(sqla.String(100), nullable=False)
    village = sqla.Column(sqla.String(100), nullable=False)
    region = sqla.Column(sqla.String(100), nullable=False)
    membershipTypeID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_membertype.id'))
    membershipSubCatID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_membershipsubcat.id'))
    date_joined = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contactPersons = sqla_orm.relationship('ContactPersons', back_populates='memberContact')
    membershipType = sqla_orm.relationship('MemberType', back_populates='typeMember')
    membershipSubCategory = sqla_orm.relationship('MemberSubCategory', back_populates='membersubcat')
    memberApplication = sqla_orm.relationship('MemberApplication', back_populates='member', lazy='noload')

    def __repr__(self):
        return '<Members {}>'.format(self.text)


class MemberType(db.Model):
    __tablename__ = 'netp_membertype'

    id = sqla.Column(sqla.Integer, primary_key=True)
    title = sqla.Column(sqla.String(255), unique=True)

    typeMember = sqla_orm.relationship('Members', back_populates='membershipType', lazy='noload')
    subCategory = sqla_orm.relationship('MemberSubCategory', back_populates='memberType')

    def __repr__(self):
        return '<MemberType {}>'.format(self.title)


class MemberSubCategory(db.Model):
    __tablename__ = 'netp_membershipsubcat'

    id = sqla.Column(sqla.Integer, primary_key=True)
    title = sqla.Column(sqla.String(255), unique=True)
    typeID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_membertype.id'))

    memberType = sqla_orm.relationship('MemberType', back_populates='subCategory', lazy='noload')
    membersubcat = sqla_orm.relationship('Members', back_populates='membershipSubCategory', lazy='noload')

    def __repr__(self):
        return '<MemberSubCategory {}>'.format(self.title)


class ContactPersons(Updateable, db.Model):
    __tablename__ = 'netp_contactpersons'

    id = sqla.Column(sqla.Integer, primary_key=True)
    c_firstName = sqla.Column(sqla.String(100), nullable=False)
    c_lastName = sqla.Column(sqla.String(100), nullable=False)
    c_position = sqla.Column(sqla.String(100), nullable=False)
    c_phone = sqla.Column(sqla.String(100), nullable=False)
    c_workphone = sqla.Column(sqla.String(100), nullable=False)
    c_email = sqla.Column(sqla.String(100), nullable=True)
    c_memberID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_members.id'), index=True)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)

    memberContact = sqla_orm.relationship('Members', back_populates='contactPersons')

    def __repr__(self):
        return 'ContactsPersons {}'.format(self.text)
