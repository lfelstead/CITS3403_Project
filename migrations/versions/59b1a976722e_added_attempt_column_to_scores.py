"""Added attempt column to scores

Revision ID: 59b1a976722e
Revises: 44055b1e4b4d
Create Date: 2021-05-11 22:20:23.522523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59b1a976722e'
down_revision = '44055b1e4b4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scores', sa.Column('attempt', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scores', 'attempt')
    # ### end Alembic commands ###