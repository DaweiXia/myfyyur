"""empty message

Revision ID: f8ceb1fb468a
Revises: 77886953b46b
Create Date: 2019-10-27 18:40:09.366220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8ceb1fb468a'
down_revision = '77886953b46b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.drop_column('Artist', 'upcomint_shows_count')
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.drop_column('Venue', 'upcomint_shows_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('upcomint_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'upcoming_shows_count')
    op.add_column('Artist', sa.Column('upcomint_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'upcoming_shows_count')
    # ### end Alembic commands ###
