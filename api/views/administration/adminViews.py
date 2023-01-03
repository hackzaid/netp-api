from apifairy.decorators import other_responses
from flask import Blueprint, abort, g
from apifairy import authenticate, body, response
from flask_login import current_user

from api import db
from api.models.administration.adminModels import User, Role, Group
from api.schemas.administration.adminSchemas import UserSchema, UpdateUserSchema, GroupSchema, RoleSchema
from api.auth import token_auth
from api.decorators import paginated_response

users = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


@users.route('/users', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
def new(args):
    """Register a new user"""
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    return user


@users.route('/users', methods=['GET'])
@authenticate(token_auth, role=['user', ['admin']])
@paginated_response(users_schema)
def all():
    """Retrieve all users"""
    return User.select()


@users.route('/user/role', methods=['POST'])
@authenticate(token_auth, role=['user', ['admin']])
def test_roles():
    """Assign Role to User"""
    return "Hello {}, you are an admin or normal user!".format(token_auth.current_user())


@users.route('/users/<int:id>', methods=['GET'])
@authenticate(token_auth, role=['user', ['moderator', 'admin']])
@response(user_schema)
@other_responses({404: 'User not found'})
def get(id):
    """Retrieve a user by id"""
    return db.session.get(User, id) or abort(404)


@users.route('/users/<username>', methods=['GET'])
@authenticate(token_auth, role=['user', ['moderator', 'admin']])
@response(user_schema)
@other_responses({404: 'User not found'})
def get_by_username(username):
    """Retrieve a user by username"""
    return db.session.scalar(User.select().filter_by(username=username)) or \
           abort(404)


@users.route('/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    return token_auth.current_user()


@users.route('/me', methods=['PUT'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def put(data):
    """Edit user information"""
    user = token_auth.current_user()
    if 'password' in data and ('old_password' not in data or
                               not user.verify_password(data['old_password'])):
        abort(400)
    user.update(data)
    db.session.commit()
    return user


@users.route('/user/role', methods=['POST'])
@authenticate(token_auth, role=['admin'])
@body(role_schema)
@response(role_schema)
def role_add(args):
    """Add User Roles"""
    role = Role(**args)
    role.allowances = dict(
        members='r',
        secret_members=None  # no authorization
    )
    db.session.add(role)
    db.session.commit()
    return role
