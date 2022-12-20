"""empty message

Revision ID: 0cdcedb8a181
Revises: a19c401063d0
Create Date: 2022-12-20 23:02:42.223831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cdcedb8a181'
down_revision = 'a19c401063d0'
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
    op.create_index(op.f('ix_netp_members_membershipID'), 'netp_members', ['membershipID'], unique=False)
    op.create_table('netp_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productName', sa.String(length=100), nullable=False),
    sa.Column('categoryID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoryID'], ['netp_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netp_product_categoryID'), 'netp_product', ['categoryID'], unique=False)
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
    op.drop_index(op.f('ix_netp_product_categoryID'), table_name='netp_product')
    op.drop_table('netp_product')
    op.drop_index(op.f('ix_netp_members_membershipID'), table_name='netp_members')
    op.drop_table('netp_members')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('netp_membertype')
    op.drop_table('netp_category')
    # ### end Alembic commands ###
