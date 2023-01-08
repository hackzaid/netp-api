"""empty message

Revision ID: df16013b4b2c
Revises: e252534e95d3
Create Date: 2023-01-03 23:40:39.592958

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'df16013b4b2c'
down_revision = 'e252534e95d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('netp_application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regNo', sa.String(length=255), nullable=True),
    sa.Column('memberID', sa.Integer(), nullable=True),
    sa.Column('membershipID', sa.Integer(), nullable=True),
    sa.Column('memberSubCategoryID', sa.Integer(), nullable=True),
    sa.Column('productID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['memberID'], ['netp_members.id'], ),
    sa.ForeignKeyConstraint(['memberSubCategoryID'], ['netp_membershipsubcat.id'], ),
    sa.ForeignKeyConstraint(['membershipID'], ['netp_membertype.id'], ),
    sa.ForeignKeyConstraint(['productID'], ['netp_product.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('regNo')
    )
    op.create_index(op.f('ix_netp_application_memberID'), 'netp_application', ['memberID'], unique=False)
    op.create_index(op.f('ix_netp_application_memberSubCategoryID'), 'netp_application', ['memberSubCategoryID'], unique=False)
    op.create_index(op.f('ix_netp_application_membershipID'), 'netp_application', ['membershipID'], unique=False)
    op.create_index(op.f('ix_netp_application_productID'), 'netp_application', ['productID'], unique=False)

    op.drop_table('netp_productcategories')
    op.create_foreign_key(None, 'netp_contactpersons', 'netp_members', ['c_memberID'], ['id'])
    op.create_foreign_key(None, 'netp_members', 'netp_membertype', ['membershipID'], ['id'])
    op.create_foreign_key(None, 'netp_membershipsubcat', 'netp_membertype', ['typeID'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'netp_category', ['categoryID'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_membershipsubcat', type_='foreignkey')
    op.drop_constraint(None, 'netp_members', type_='foreignkey')
    op.drop_constraint(None, 'netp_contactpersons', type_='foreignkey')

    op.drop_index(op.f('ix_netp_application_productID'), table_name='netp_application')
    op.drop_index(op.f('ix_netp_application_membershipID'), table_name='netp_application')
    op.drop_index(op.f('ix_netp_application_memberSubCategoryID'), table_name='netp_application')
    op.drop_index(op.f('ix_netp_application_memberID'), table_name='netp_application')
    op.drop_table('netp_application')
    # ### end Alembic commands ###
