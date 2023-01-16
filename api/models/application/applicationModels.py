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

from api.models.models import Updateable

from api.app import db


class MemberApplication(db.Model, Updateable):
    __tablename__ = 'netp_application'

    id = sqla.Column(sqla.Integer, primary_key=True)
    regNo = sqla.Column(sqla.String(255), unique=True)
    memberID = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'), index=True)
    productID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_product.id'), index=True)
    businessType = sqla.Column(sqla.String(155))
    companyDescription = sqla.Column(sqla.String(155))
    exportNo = sqla.Column(sqla.String(155), unique=True)
    applicationStatus = sqla.Column(sqla.String(155))
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applicationAttachments = sqla_orm.relationship("ApplicationFiles", back_populates='application')
    member = sqla_orm.relationship("User", back_populates='memberApplication', lazy='noload')
    majorProduct = sqla_orm.relationship("Product", back_populates='applicationProduct', lazy='noload')


class ApplicationFiles(db.Model):
    __tablename__ = 'netp_application_files'

    id = sqla.Column(sqla.Integer, primary_key=True)
    companyRegCert = sqla.Column(sqla.String(155), unique=True)
    exportRegCert = sqla.Column(sqla.String(155), unique=True)
    companyProfile = sqla.Column(sqla.String(155), unique=True)
    applicationID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_application.id'), index=True)

    application = sqla_orm.relationship("MemberApplication", back_populates='applicationAttachments')
