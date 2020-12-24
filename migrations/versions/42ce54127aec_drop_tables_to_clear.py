"""Drop tables to clear

Revision ID: 42ce54127aec
Revises: 2c94e02de386
Create Date: 2020-08-23 19:59:18.713134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42ce54127aec'
down_revision = '2c94e02de386'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('days_hobbies_table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('days_hobbies_table',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('day_id', sa.INTEGER(), nullable=False),
    sa.Column('hobby_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['day_id'], ['day.id'], ),
    sa.ForeignKeyConstraint(['hobby_id'], ['hobby.id'], ),
    sa.PrimaryKeyConstraint('id', 'day_id', 'hobby_id')
    )
    # ### end Alembic commands ###
