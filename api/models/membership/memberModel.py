from datetime import datetime, timedelta
from hashlib import md5
import secrets
from time import time

from flask import current_app, url_for
import jwt
import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm
from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Members(Updateable, db.Model):
    __tablename__ = 'netp_members'

    id = sqla.Column(sqla.Integer, primary_key=True)
    regNo = sqla.Column(sqla.BigInteger, unique=True, nullable=False)
    firstName = sqla.Column(sqla.String(100), nullable=False)
    lastName = sqla.Column(sqla.String(100), nullable=False)
    village = sqla.Column(sqla.String(100), nullable=False)
    region = sqla.Column(sqla.String(100), nullable=False)
    date_joined = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contactPersons = sqla_orm.relationship('ContactPersons', back_populates='memberContact')

    def __repr__(self):
        return '<Members {}>'.format(self.text)


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
