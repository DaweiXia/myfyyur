"""empty message

Revision ID: c7dc0adb4902
Revises: 25d3a04ec9a3
Create Date: 2019-10-27 13:40:42.628381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7dc0adb4902'
down_revision = '25d3a04ec9a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('past_shows', sa.ARRAY(sa.JSON()), nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows', sa.ARRAY(sa.JSON()), nullable=True))
    op.add_column('Artist', sa.Column('upcomint_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('webstie', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'webstie')
    op.drop_column('Artist', 'upcomint_shows_count')
    op.drop_column('Artist', 'upcoming_shows')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'past_shows')
    # ### end Alembic commands ###
