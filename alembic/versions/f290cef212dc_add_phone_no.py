"""add phone no

Revision ID: f290cef212dc
Revises: f94a983107f2
Create Date: 2023-04-24 23:48:29.980009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f290cef212dc'
down_revision = 'f94a983107f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_no', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_no')
    # ### end Alembic commands ###
