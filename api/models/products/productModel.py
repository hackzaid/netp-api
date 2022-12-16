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

productCategories = sqla.Table(
    'netp_productCategories',
    db.Model.metadata,
    sqla.Column('product_id', sqla.Integer, sqla.ForeignKey('netp_product.id')),
    sqla.Column('netp_category', sqla.Integer, sqla.ForeignKey('netp_category.id'))
)


class Category(db.Model):
    __tablename__ = 'netp_category'

    id = sqla.Column(sqla.Integer, primary_key=True)
    catName = sqla.Column(sqla.String(100), nullable=False)
    catDescription = sqla.Column(sqla.String(150), nullable=True)

    def __repr__(self):
        return "Category {}".format(self.text)


class Product(db.Model):
    __tablename__ = 'netp_product'

    id = sqla.Column(sqla.Integer, primary_key=True)
    productName = sqla.Column(sqla.String(100), nullable=False)
    categoryID = sqla.Column(sqla.Integer, sqla.ForeignKey('netp_category.id'), index=True)

    productCategory = sqla_orm.relationship("Category", secondary=productCategories, backref='netp_product')

    def __repr__(self):
        return "Product {}".format(self.text)
