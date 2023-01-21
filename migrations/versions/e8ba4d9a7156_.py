"""empty message

Revision ID: e8ba4d9a7156
Revises: b5201963a6d4
Create Date: 2023-01-20 12:48:13.918036

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize


# revision identifiers, used by Alembic.
revision = 'e8ba4d9a7156'
down_revision = 'b5201963a6d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('netp_answers', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_answers', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_answers', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_answers', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_answers', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_answers', 'netp_inspections', ['inspection_id'], ['id'])
    op.create_foreign_key(None, 'netp_answers', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_answers', 'netp_questions', ['question_id'], ['id'])
    op.create_foreign_key(None, 'netp_answers', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'netp_application', 'netp_product', ['productID'], ['id'])
    op.create_foreign_key(None, 'netp_application', 'users', ['memberID'], ['id'])
    op.create_foreign_key(None, 'netp_application_files', 'netp_application', ['applicationID'], ['id'])
    op.create_foreign_key(None, 'netp_contactpersons', 'users', ['c_memberID'], ['id'])
    op.add_column('netp_inspection_form_sections', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspection_form_sections', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspection_form_sections', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspection_form_sections', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspection_form_sections', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_inspection_form_sections', 'netp_inspection_forms', ['inspection_form_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspection_form_sections', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspection_form_sections', 'users', ['owner_id'], ['id'])
    op.add_column('netp_inspection_forms', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspection_forms', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspection_forms', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspection_forms', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspection_forms', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_inspection_forms', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspection_forms', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspection_inspectors', 'netp_inspectors', ['inspector_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspection_inspectors', 'netp_inspections', ['inspection_id'], ['id'])
    op.add_column('netp_inspections', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspections', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspections', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspections', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspections', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_inspections', 'netp_inspection_forms', ['inspection_form_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspections', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspections', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspections', 'users', ['user_id'], ['id'])
    op.add_column('netp_inspectors', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspectors', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspectors', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_inspectors', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_inspectors', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_inspectors', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'netp_inspectors', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_member_details', 'netp_membertype', ['membershipTypeID'], ['id'])
    op.create_foreign_key(None, 'netp_member_details', 'users', ['userID'], ['id'])
    op.create_foreign_key(None, 'netp_member_details', 'netp_membershipsubcat', ['membershipSubCatID'], ['id'])
    op.create_foreign_key(None, 'netp_membershipsubcat', 'netp_membertype', ['typeID'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'netp_category', ['categoryID'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'users', ['added_by'], ['id'])
    op.add_column('netp_questions', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_questions', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_questions', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_questions', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_questions', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_questions', 'netp_inspection_form_sections', ['inspection_form_section_id'], ['id'])
    op.create_foreign_key(None, 'netp_questions', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'netp_questions', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'ntep_user_group', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'ntep_user_group', 'ntep_groups', ['group_id'], ['id'])
    op.create_foreign_key(None, 'ntep_user_role', 'ntep_roles', ['role_id'], ['id'])
    op.create_foreign_key(None, 'ntep_user_role', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'tokens', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tokens', type_='foreignkey')
    op.drop_constraint(None, 'ntep_user_role', type_='foreignkey')
    op.drop_constraint(None, 'ntep_user_role', type_='foreignkey')
    op.drop_constraint(None, 'ntep_user_group', type_='foreignkey')
    op.drop_constraint(None, 'ntep_user_group', type_='foreignkey')
    op.drop_constraint(None, 'netp_questions', type_='foreignkey')
    op.drop_constraint(None, 'netp_questions', type_='foreignkey')
    op.drop_constraint(None, 'netp_questions', type_='foreignkey')
    op.drop_column('netp_questions', 'group_permissions')
    op.drop_column('netp_questions', 'group_id')
    op.drop_column('netp_questions', 'owner_permissions')
    op.drop_column('netp_questions', 'owner_id')
    op.drop_column('netp_questions', 'other_permissions')
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_membershipsubcat', type_='foreignkey')
    op.drop_constraint(None, 'netp_member_details', type_='foreignkey')
    op.drop_constraint(None, 'netp_member_details', type_='foreignkey')
    op.drop_constraint(None, 'netp_member_details', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspectors', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspectors', type_='foreignkey')
    op.drop_column('netp_inspectors', 'group_permissions')
    op.drop_column('netp_inspectors', 'group_id')
    op.drop_column('netp_inspectors', 'owner_permissions')
    op.drop_column('netp_inspectors', 'owner_id')
    op.drop_column('netp_inspectors', 'other_permissions')
    op.drop_constraint(None, 'netp_inspections', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspections', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspections', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspections', type_='foreignkey')
    op.drop_column('netp_inspections', 'group_permissions')
    op.drop_column('netp_inspections', 'group_id')
    op.drop_column('netp_inspections', 'owner_permissions')
    op.drop_column('netp_inspections', 'owner_id')
    op.drop_column('netp_inspections', 'other_permissions')
    op.drop_constraint(None, 'netp_inspection_inspectors', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspection_inspectors', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspection_forms', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspection_forms', type_='foreignkey')
    op.drop_column('netp_inspection_forms', 'group_permissions')
    op.drop_column('netp_inspection_forms', 'group_id')
    op.drop_column('netp_inspection_forms', 'owner_permissions')
    op.drop_column('netp_inspection_forms', 'owner_id')
    op.drop_column('netp_inspection_forms', 'other_permissions')
    op.drop_constraint(None, 'netp_inspection_form_sections', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspection_form_sections', type_='foreignkey')
    op.drop_constraint(None, 'netp_inspection_form_sections', type_='foreignkey')
    op.drop_column('netp_inspection_form_sections', 'group_permissions')
    op.drop_column('netp_inspection_form_sections', 'group_id')
    op.drop_column('netp_inspection_form_sections', 'owner_permissions')
    op.drop_column('netp_inspection_form_sections', 'owner_id')
    op.drop_column('netp_inspection_form_sections', 'other_permissions')
    op.drop_constraint(None, 'netp_contactpersons', type_='foreignkey')
    op.drop_constraint(None, 'netp_application_files', type_='foreignkey')
    op.drop_constraint(None, 'netp_application', type_='foreignkey')
    op.drop_constraint(None, 'netp_application', type_='foreignkey')
    op.drop_constraint(None, 'netp_answers', type_='foreignkey')
    op.drop_constraint(None, 'netp_answers', type_='foreignkey')
    op.drop_constraint(None, 'netp_answers', type_='foreignkey')
    op.drop_constraint(None, 'netp_answers', type_='foreignkey')
    op.drop_column('netp_answers', 'group_permissions')
    op.drop_column('netp_answers', 'group_id')
    op.drop_column('netp_answers', 'owner_permissions')
    op.drop_column('netp_answers', 'owner_id')
    op.drop_column('netp_answers', 'other_permissions')
    # ### end Alembic commands ###
