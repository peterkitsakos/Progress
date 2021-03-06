"""Continued work on hobby/day mamany-many relationship

Revision ID: bf4253f03eec
Revises: a4695aef3786
Create Date: 2020-08-17 20:08:32.348578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf4253f03eec'
down_revision = 'a4695aef3786'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('day', schema=None) as batch_op:
        batch_op.add_column(sa.Column('curr', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('past', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('day', schema=None) as batch_op:
        batch_op.drop_column('past')
        batch_op.drop_column('curr')

    # ### end Alembic commands ###
