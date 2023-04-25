"""add content column to posts

Revision ID: ee65802a99c8
Revises: 7f2f79909a3f
Create Date: 2023-04-24 23:12:56.609312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee65802a99c8'
down_revision = '7f2f79909a3f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
