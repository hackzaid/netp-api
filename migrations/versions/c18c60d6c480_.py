"""empty message

Revision ID: c18c60d6c480
Revises: 364838d0c20a
Create Date: 2023-01-03 15:44:15.821839

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize

# revision identifiers, used by Alembic.
revision = 'c18c60d6c480'
down_revision = '364838d0c20a'
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
    sa.Column('allowances', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('first_seen', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('netp_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regNo', sa.BigInteger(), nullable=False),
    sa.Column('firstName', sa.String(length=100), nullable=False),
    sa.Column('lastName', sa.String(length=100), nullable=False),
    sa.Column('village', sa.String(length=100), nullable=False),
    sa.Column('region', sa.String(length=100), nullable=False),
    sa.Column('membershipID', sa.Integer(), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['membershipID'], ['netp_membertype.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('regNo')
    )
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
    sa.ForeignKeyConstraint(['categoryID'], ['netp_category.id'], ),
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
    sa.ForeignKeyConstraint(['c_memberID'], ['netp_members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_contactpersons_c_memberID'), 'netp_contactpersons', ['c_memberID'], unique=False)
    op.create_table('netp_productCategories',
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('netp_category', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['netp_category'], ['netp_category.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['netp_product.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('netp_productCategories')
    op.drop_index(op.f('ix_netp_contactpersons_c_memberID'), table_name='netp_contactpersons')
    op.drop_table('netp_contactpersons')
    op.drop_index(op.f('ix_tokens_user_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_refresh_token'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_table('ntep_user_role')
    op.drop_table('ntep_user_group')
    op.drop_index(op.f('ix_netp_product_categoryID'), table_name='netp_product')
    op.drop_table('netp_product')
    op.drop_table('netp_membershipsubcat')
    op.drop_table('netp_members')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('ntep_roles')
    op.drop_table('ntep_groups')
    op.drop_table('netp_membertype')
    op.drop_table('netp_category')
    # ### end Alembic commands ###
