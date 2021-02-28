"""empty message

Revision ID: 6d109e137850
Revises: 762402052503
Create Date: 2021-02-25 21:37:46.055900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d109e137850'
down_revision = '762402052503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('Type', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('characters_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('orbital', sa.Integer(), nullable=False),
    sa.Column('period', sa.Integer(), nullable=False),
    sa.Column('rotation_period', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('characters_id'),
    sa.UniqueConstraint('diameter'),
    sa.UniqueConstraint('orbital'),
    sa.UniqueConstraint('period'),
    sa.UniqueConstraint('population')
    )
    op.create_table('planets',
    sa.Column('planets_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('birth', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('skin', sa.String(length=250), nullable=False),
    sa.Column('eye_color', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('planets_id'),
    sa.UniqueConstraint('gender')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planets')
    op.drop_table('people')
    op.drop_table('favorites')
    # ### end Alembic commands ###