from datetime import datetime, timedelta
from hashlib import md5
import secrets
from time import time

from flask import current_app, url_for
import jwt
import sqlalchemy as sqla
from flask_authorize import PermissionsMixin
from sqlalchemy import orm as sqla_orm
from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db


class Category(db.Model):
    __tablename__ = 'netp_category'

    id = sqla.Column(sqla.Integer, primary_key=True)
    catName = sqla.Column(sqla.String(100), nullable=False)
    catDescription = sqla.Column(sqla.String(150), nullable=True)

    def __repr__(self):
        return "Category {}".format(self.catName)


class Product(db.Model, PermissionsMixin):
    __tablename__ = 'netp_product'
    __permissions__ = dict(
        owner=['read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    productName = sqla.Column(sqla.String(100), nullable=False)
    categoryID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_category.id'), index=True)
    date_added = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    productCategory = sqla_orm.relationship("Category", backref='netp_product')
    applicationProduct = sqla_orm.relationship("MemberApplication", back_populates='majorProduct', lazy='noload')

    def __repr__(self):
        return "Product {}".format(self.productName)
