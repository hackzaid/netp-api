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
    memberID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_members.id'), index=True)
    membershipID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_membertype.id'), index=True)
    memberSubCategoryID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_membershipsubcat.id'), index=True)
    productID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_product.id'), index=True)

    member = sqla_orm.relationship("Members", back_populates='memberApplication', lazy='noload')
    membershipType = sqla_orm.relationship("MemberType", back_populates='applicationMembership', lazy='noload')
    memberSubCategory = sqla_orm.relationship("MemberSubCategory", back_populates='applicationSubCat', lazy='noload')
    majorProduct = sqla_orm.relationship("Product", back_populates='applicationProduct', lazy='noload')
