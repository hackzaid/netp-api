"""empty message

Revision ID: 2cc9aaa283fc
Revises: 
Create Date: 2023-01-16 14:44:17.811841

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize


# revision identifiers, used by Alembic.
revision = '2cc9aaa283fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('netp_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('catName', sa.String(length=100), nullable=False),
    sa.Column('catDescription', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('netp_inspection_forms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('additional_details', sa.String(length=1000), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('netp_inspectors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('netp_membertype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('ntep_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('restrictions', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ntep_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('restrictions', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=100), nullable=False),
    sa.Column('lastName', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('first_seen', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('is_member', sa.Boolean(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('confirmed_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('netp_contactpersons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('c_firstName', sa.String(length=100), nullable=False),
    sa.Column('c_lastName', sa.String(length=100), nullable=False),
    sa.Column('c_position', sa.String(length=100), nullable=False),
    sa.Column('c_phone', sa.String(length=100), nullable=False),
    sa.Column('c_workphone', sa.String(length=100), nullable=False),
    sa.Column('c_email', sa.String(length=100), nullable=True),
    sa.Column('c_memberID', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['c_memberID'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_contactpersons_c_memberID'), 'netp_contactpersons', ['c_memberID'], unique=False)
    op.create_table('netp_inspection_form_sections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('section_no', sa.Integer(), nullable=False),
    sa.Column('inspection_form_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inspection_form_id'], ['netp_inspection_forms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_inspection_form_sections_inspection_form_id'), 'netp_inspection_form_sections', ['inspection_form_id'], unique=False)
    op.create_table('netp_inspections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inspection_form_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['inspection_form_id'], ['netp_inspection_forms.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_inspections_inspection_form_id'), 'netp_inspections', ['inspection_form_id'], unique=False)
    op.create_index(op.f('ix_netp_inspections_user_id'), 'netp_inspections', ['user_id'], unique=False)
    op.create_table('netp_membershipsubcat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('typeID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['typeID'], ['netp_membertype.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('netp_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productName', sa.String(length=100), nullable=False),
    sa.Column('categoryID', sa.Integer(), nullable=True),
    sa.Column('added_by', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['categoryID'], ['netp_category.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['ntep_groups.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_product_categoryID'), 'netp_product', ['categoryID'], unique=False)
    op.create_table('ntep_user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['ntep_groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('ntep_user_role',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['ntep_roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(length=64), nullable=False),
    sa.Column('access_expiration', sa.DateTime(), nullable=False),
    sa.Column('refresh_token', sa.String(length=64), nullable=False),
    sa.Column('refresh_expiration', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_access_token'), 'tokens', ['access_token'], unique=False)
    op.create_index(op.f('ix_tokens_refresh_token'), 'tokens', ['refresh_token'], unique=False)
    op.create_index(op.f('ix_tokens_user_id'), 'tokens', ['user_id'], unique=False)
    op.create_table('netp_application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regNo', sa.String(length=255), nullable=True),
    sa.Column('memberID', sa.Integer(), nullable=True),
    sa.Column('productID', sa.Integer(), nullable=True),
    sa.Column('businessType', sa.String(length=155), nullable=True),
    sa.Column('companyDescription', sa.String(length=155), nullable=True),
    sa.Column('exportNo', sa.String(length=155), nullable=True),
    sa.Column('applicationStatus', sa.String(length=155), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['memberID'], ['users.id'], ),
    sa.ForeignKeyConstraint(['productID'], ['netp_product.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('exportNo'),
    sa.UniqueConstraint('regNo')
    )
    op.create_index(op.f('ix_netp_application_memberID'), 'netp_application', ['memberID'], unique=False)
    op.create_index(op.f('ix_netp_application_productID'), 'netp_application', ['productID'], unique=False)
    op.create_table('netp_inspection_inspectors',
    sa.Column('inspector_id', sa.Integer(), nullable=True),
    sa.Column('inspection_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inspection_id'], ['netp_inspections.id'], ),
    sa.ForeignKeyConstraint(['inspector_id'], ['netp_inspectors.id'], )
    )
    op.create_table('netp_member_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regNo', sa.BigInteger(), nullable=False),
    sa.Column('village', sa.String(length=100), nullable=False),
    sa.Column('region', sa.String(length=100), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('membershipTypeID', sa.Integer(), nullable=True),
    sa.Column('membershipSubCatID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['membershipSubCatID'], ['netp_membershipsubcat.id'], ),
    sa.ForeignKeyConstraint(['membershipTypeID'], ['netp_membertype.id'], ),
    sa.ForeignKeyConstraint(['userID'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('regNo')
    )
    op.create_index(op.f('ix_netp_member_details_userID'), 'netp_member_details', ['userID'], unique=False)
    op.create_table('netp_questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('inspection_form_section_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inspection_form_section_id'], ['netp_inspection_form_sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_questions_inspection_form_section_id'), 'netp_questions', ['inspection_form_section_id'], unique=False)
    op.create_table('netp_answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=100), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('inspection_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['inspection_id'], ['netp_inspections.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['netp_questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_answers_inspection_id'), 'netp_answers', ['inspection_id'], unique=False)
    op.create_index(op.f('ix_netp_answers_question_id'), 'netp_answers', ['question_id'], unique=False)
    op.create_table('netp_application_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('companyRegCert', sa.String(length=155), nullable=True),
    sa.Column('exportRegCert', sa.String(length=155), nullable=True),
    sa.Column('companyProfile', sa.String(length=155), nullable=True),
    sa.Column('applicationID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['applicationID'], ['netp_application.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('companyProfile'),
    sa.UniqueConstraint('companyRegCert'),
    sa.UniqueConstraint('exportRegCert')
    )
    op.create_index(op.f('ix_netp_application_files_applicationID'), 'netp_application_files', ['applicationID'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_netp_application_files_applicationID'), table_name='netp_application_files')
    op.drop_table('netp_application_files')
    op.drop_index(op.f('ix_netp_answers_question_id'), table_name='netp_answers')
    op.drop_index(op.f('ix_netp_answers_inspection_id'), table_name='netp_answers')
    op.drop_table('netp_answers')
    op.drop_index(op.f('ix_netp_questions_inspection_form_section_id'), table_name='netp_questions')
    op.drop_table('netp_questions')
    op.drop_index(op.f('ix_netp_member_details_userID'), table_name='netp_member_details')
    op.drop_table('netp_member_details')
    op.drop_table('netp_inspection_inspectors')
    op.drop_index(op.f('ix_netp_application_productID'), table_name='netp_application')
    op.drop_index(op.f('ix_netp_application_memberID'), table_name='netp_application')
    op.drop_table('netp_application')
    op.drop_index(op.f('ix_tokens_user_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_refresh_token'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_table('ntep_user_role')
    op.drop_table('ntep_user_group')
    op.drop_index(op.f('ix_netp_product_categoryID'), table_name='netp_product')
    op.drop_table('netp_product')
    op.drop_table('netp_membershipsubcat')
    op.drop_index(op.f('ix_netp_inspections_user_id'), table_name='netp_inspections')
    op.drop_index(op.f('ix_netp_inspections_inspection_form_id'), table_name='netp_inspections')
    op.drop_table('netp_inspections')
    op.drop_index(op.f('ix_netp_inspection_form_sections_inspection_form_id'), table_name='netp_inspection_form_sections')
    op.drop_table('netp_inspection_form_sections')
    op.drop_index(op.f('ix_netp_contactpersons_c_memberID'), table_name='netp_contactpersons')
    op.drop_table('netp_contactpersons')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('ntep_roles')
    op.drop_table('ntep_groups')
    op.drop_table('netp_membertype')
    op.drop_table('netp_inspectors')
    op.drop_table('netp_inspection_forms')
    op.drop_table('netp_category')
    # ### end Alembic commands ###
