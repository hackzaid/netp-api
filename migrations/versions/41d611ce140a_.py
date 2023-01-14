"""empty message

Revision ID: 41d611ce140a
Revises: b34ad31377eb
Create Date: 2023-01-14 14:50:59.242758

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize


# revision identifiers, used by Alembic.
revision = '41d611ce140a'
down_revision = 'b34ad31377eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'netp_application', 'users', ['memberID'], ['id'])
    op.create_foreign_key(None, 'netp_application', 'netp_product', ['productID'], ['id'])
    op.create_foreign_key(None, 'netp_contactpersons', 'users', ['c_memberID'], ['id'])
    op.create_foreign_key(None, 'netp_member_details', 'users', ['userID'], ['id'])
    op.create_foreign_key(None, 'netp_member_details', 'netp_membershipsubcat', ['membershipSubCatID'], ['id'])
    op.create_foreign_key(None, 'netp_member_details', 'netp_membertype', ['membershipTypeID'], ['id'])
    op.create_foreign_key(None, 'netp_membershipsubcat', 'netp_membertype', ['typeID'], ['id'])
    op.add_column('netp_product', sa.Column('other_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_product', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('netp_product', sa.Column('owner_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.add_column('netp_product', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('netp_product', sa.Column('group_permissions', flask_authorize.mixins.PipedList(), nullable=True))
    op.create_foreign_key(None, 'netp_product', 'users', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'netp_category', ['categoryID'], ['id'])
    op.create_foreign_key(None, 'netp_product', 'ntep_groups', ['group_id'], ['id'])
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
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_constraint(None, 'netp_product', type_='foreignkey')
    op.drop_column('netp_product', 'group_permissions')
    op.drop_column('netp_product', 'group_id')
    op.drop_column('netp_product', 'owner_permissions')
    op.drop_column('netp_product', 'owner_id')
    op.drop_column('netp_product', 'other_permissions')
    op.drop_constraint(None, 'netp_membershipsubcat', type_='foreignkey')
    op.drop_constraint(None, 'netp_member_details', type_='foreignkey')
    op.drop_constraint(None, 'netp_member_details', type_='foreignkey')
    op.drop_constraint(None, 'netp_member_details', type_='foreignkey')
    op.drop_constraint(None, 'netp_contactpersons', type_='foreignkey')
    op.drop_constraint(None, 'netp_application', type_='foreignkey')
    op.drop_constraint(None, 'netp_application', type_='foreignkey')
    # ### end Alembic commands ###
