from apifairy.decorators import other_responses
from flask import Blueprint, abort, g
from apifairy import authenticate, body, response
from flask_login import current_user

from api import db
from api.app import authorize
from api.models.administration.adminModels import User, Role, Group, UserRole
from api.schemas.administration.adminSchemas import UserSchema, UpdateUserSchema, GroupSchema, RoleSchema, \
    AssignRoleSchema
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

assign_role_schema = AssignRoleSchema()


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


@users.route('/user/manage/role/', methods=['POST'])
@authenticate(token_auth, role=['user', ['admin']])
@body(assign_role_schema)
@response(role_schema)
def assign_roles(args):
    """Assign Role to User"""
    user = db.session.get(User, 1)
    role = db.session.get(Role, assign_role_schema.role_id)
    user.roles.append(role)
    db.session.add(role)
    db.session.commit()
    return {'user': 'firstName {}'.format(user.firstName)}


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
@authenticate(token_auth)
@body(role_schema)
@response(role_schema)
def role_add(args):
    """Add User Roles"""
    role = Role(**args)
    role.restrictions = dict(
        netp_product=['create', 'update', 'delete']
    )
    db.session.add(role)
    db.session.commit()
    return role


@users.route('/roles', methods=['GET'])
@authenticate(token_auth)
@paginated_response(role_schema)
def get_roles():
    """Get All Roles"""
    return Role.select()
