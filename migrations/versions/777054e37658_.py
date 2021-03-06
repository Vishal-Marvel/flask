"""empty message

Revision ID: 777054e37658
Revises: 366a785ef3d6
Create Date: 2022-01-27 13:32:39.830771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '777054e37658'
down_revision = '366a785ef3d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('slug', sa.String(length=200), nullable=True))
    op.drop_column('posts', 'slig')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('slig', sa.VARCHAR(length=200), nullable=True))
    op.drop_column('posts', 'slug')
    # ### end Alembic commands ###
