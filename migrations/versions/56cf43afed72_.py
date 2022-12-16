"""empty message

Revision ID: 56cf43afed72
Revises: c7f167c12181
Create Date: 2022-12-16 11:50:51.133267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56cf43afed72'
down_revision = 'c7f167c12181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'followers', 'users', ['followed_id'], ['id'])
    op.create_foreign_key(None, 'followers', 'users', ['follower_id'], ['id'])
    op.add_column('netp_contactpersons', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'netp_contactpersons', 'netp_members', ['c_memberID'], ['id'])
    op.add_column('netp_members', sa.Column('date_joined', sa.DateTime(), nullable=True))
    op.add_column('netp_members', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'tokens', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tokens', type_='foreignkey')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('netp_members', 'updated_on')
    op.drop_column('netp_members', 'date_joined')
    op.drop_constraint(None, 'netp_contactpersons', type_='foreignkey')
    op.drop_column('netp_contactpersons', 'created_on')
    op.drop_constraint(None, 'followers', type_='foreignkey')
    op.drop_constraint(None, 'followers', type_='foreignkey')
    # ### end Alembic commands ###