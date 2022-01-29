"""empty message

Revision ID: 366a785ef3d6
Revises: 4066a04840ac
Create Date: 2022-01-27 13:31:56.901093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '366a785ef3d6'
down_revision = '4066a04840ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('date_posted', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('slig', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'slig')
    op.drop_column('posts', 'date_posted')
    # ### end Alembic commands ###