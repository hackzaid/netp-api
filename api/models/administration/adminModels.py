from datetime import datetime, timedelta
from hashlib import md5
import secrets
from time import time

from flask import current_app, url_for
import jwt
import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin

from api.app import db


UserGroup = sqla.Table(
    'ntep_user_group',
    db.Model.metadata,
    sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('users.id')),
    sqla.Column('group_id', sqla.Integer, sqla.ForeignKey('ntep_groups.id'))
)

UserRole = sqla.Table(
    'ntep_user_role',
    db.Model.metadata,
    sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('users.id')),
    sqla.Column('role_id', sqla.Integer, sqla.ForeignKey('ntep_roles.id'))
)


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Token(db.Model):
    __tablename__ = 'tokens'

    id = sqla.Column(sqla.Integer, primary_key=True)
    access_token = sqla.Column(sqla.String(64), nullable=False, index=True)
    access_expiration = sqla.Column(sqla.DateTime, nullable=False)
    refresh_token = sqla.Column(sqla.String(64), nullable=False, index=True)
    refresh_expiration = sqla.Column(sqla.DateTime, nullable=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'),
                          index=True)

    user = sqla_orm.relationship('User', back_populates='tokens')

    def generate(self):
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=current_app.config['ACCESS_TOKEN_MINUTES'])
        self.refresh_token = secrets.token_urlsafe()
        self.refresh_expiration = datetime.utcnow() + \
            timedelta(days=current_app.config['REFRESH_TOKEN_DAYS'])

    def expire(self, delay=None):
        if delay is None:  # pragma: no branch
            # 5 second delay to allow simultaneous requests
            delay = 5 if not current_app.testing else 0
        self.access_expiration = datetime.utcnow() + timedelta(seconds=delay)
        self.refresh_expiration = datetime.utcnow() + timedelta(seconds=delay)

    @staticmethod
    def clean():
        """Remove any tokens that have been expired for more than a day."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        db.session.execute(Token.delete().where(
            Token.refresh_expiration < yesterday))


class User(Updateable, db.Model):
    __tablename__ = 'users'

    id = sqla.Column(sqla.Integer, primary_key=True)
    firstName = sqla.Column(sqla.String(100), nullable=False)
    lastName = sqla.Column(sqla.String(100), nullable=False)
    username = sqla.Column(sqla.String(64), index=True, unique=True,
                           nullable=False)
    email = sqla.Column(sqla.String(120), index=True, unique=True,
                        nullable=False)
    password_hash = sqla.Column(sqla.String(128))
    about_me = sqla.Column(sqla.String(140))
    first_seen = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    last_seen = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    is_member = sqla.Column(sqla.Boolean, default=True, nullable=False)
    is_active = sqla.Column(sqla.Boolean, default=True, nullable=False)
    created_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    updated_on = sqla.Column(
        sqla.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed = sqla.Column(sqla.Boolean, nullable=False, default=False)
    confirmed_on = sqla.Column(sqla.DateTime, default=datetime.utcnow)

    roles = sqla_orm.relationship('Role', secondary=UserRole)
    groups = sqla_orm.relationship('Group', secondary=UserGroup)
    tokens = sqla_orm.relationship('Token', back_populates='user',
                                   lazy='noload')

    product = sqla_orm.relationship("Product", primaryjoin="or_(User.id == Product.owner_id, User.id == "
                                                           "Product.added_by)")
    memberInfo = sqla_orm.relationship(
        'MemberDetails', back_populates='userDetails')
    memberApplication = sqla_orm.relationship(
        "MemberApplication", back_populates='member', lazy='noload')
    contactPersons = sqla_orm.relationship(
        'ContactPersons', back_populates='memberContact', lazy='noload')

    def user_applications_select(self):
        return "MemberApplication".select().where(sqla_orm.with_parent(self, User.memberApplication))
    #
    # def following_select(self):
    #     return User.select().where(sqla_orm.with_parent(self, User.following))
    #
    # def followers_select(self):
    #     return User.select().where(sqla_orm.with_parent(self, User.followers))
    #
    # def followed_posts_select(self):
    #     return Post.select().join(
    #         followers, (followers.c.followed_id == Post.user_id),
    #         isouter=True).group_by(Post.id).filter(
    #         sqla.or_(Post.author == self,
    #                  followers.c.follower_id == self.id))

    def __repr__(self):  # pragma: no cover
        return '<User {}>'.format(self.username)

    @property
    def url(self):
        return url_for('users.get', id=self.id)

    @property
    def avatar_url(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def generate_auth_token(self):
        token = Token(user=self)
        token.generate()
        return token

    def get_roles(self):
        role = [r.name for r in self.roles]
        return role

    def get_restrictions(self):
        group = [r.restrictions for r in self.roles]
        return group

    @staticmethod
    def verify_access_token(access_token, refresh_token=None):
        token = db.session.scalar(Token.select().filter_by(
            access_token=access_token))
        if token:
            if token.access_expiration > datetime.utcnow():
                token.user.ping()
                db.session.commit()
                return token.user

    @staticmethod
    def verify_refresh_token(refresh_token, access_token):
        token = db.session.scalar(Token.select().filter_by(
            refresh_token=refresh_token, access_token=access_token))
        if token:
            if token.refresh_expiration > datetime.utcnow():
                return token

            # someone tried to refresh with an expired token
            # revoke all tokens from this user as a precaution
            token.user.revoke_all()
            db.session.commit()

    def revoke_all(self):
        db.session.execute(Token.delete().where(Token.user == self))

    def generate_reset_token(self):
        return jwt.encode(
            {
                'exp': time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
                'reset_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def generate_confirmation_token(self):
        serializer = jwt.encode(
            {
                'exp': time() + current_app.config['CONFIRM_EMAIL_TOKEN'] * 60,
                'confirm_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return serializer

    @staticmethod
    def confirm_token(confirmation_token):
        try:
            email = jwt.decode(confirmation_token, current_app.config['SECRET_KEY'],
                               algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return email

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return db.session.scalar(User.select().filter_by(
            email=data['reset_email']))

    # def follow(self, user):
    #     if not self.is_following(user):
    #         db.session.execute(followers.insert().values(
    #             follower_id=self.id, followed_id=user.id))
    #
    # def unfollow(self, user):
    #     if self.is_following(user):
    #         db.session.execute(followers.delete().where(
    #             followers.c.follower_id == self.id,
    #             followers.c.followed_id == user.id))
    #
    # def is_following(self, user):
    #     return db.session.scalars(User.select().where(
    #         User.id == self.id, User.following.contains(
    #             user))).one_or_none() is not None


class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'ntep_groups'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(255), nullable=False, unique=True)


class Role(db.Model, RestrictionsMixin):
    __tablename__ = 'ntep_roles'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(255), nullable=False, unique=True)
