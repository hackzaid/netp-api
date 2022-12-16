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


class Post(Updateable, db.Model):
    __tablename__ = 'posts'

    id = sqla.Column(sqla.Integer, primary_key=True)
    text = sqla.Column(sqla.String(280), nullable=False)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'), index=True)

    author = sqla_orm.relationship('User', back_populates='posts', lazy='joined', primaryjoin='User.id == Post.user_id')

    def __repr__(self):  # pragma: no cover
        return '<Post {}>'.format(self.text)

    @property
    def url(self):
        return url_for('posts.get', id=self.id)
