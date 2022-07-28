"""empty message

Revision ID: 8c76fee6ae64
Revises: fbe3a8475925
Create Date: 2022-07-28 01:47:43.186549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c76fee6ae64'
down_revision = 'fbe3a8475925'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'])
    op.drop_table('roles')
    # ### end Alembic commands ###