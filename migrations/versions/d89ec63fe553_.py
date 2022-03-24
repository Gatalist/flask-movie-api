"""empty message

Revision ID: d89ec63fe553
Revises: 1a2aa0517f08
Create Date: 2022-03-17 16:12:35.878497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd89ec63fe553'
down_revision = '1a2aa0517f08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie_genre',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_genre')
    # ### end Alembic commands ###
