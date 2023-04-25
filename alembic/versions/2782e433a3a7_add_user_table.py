"""add user table

Revision ID: 2782e433a3a7
Revises: ee65802a99c8
Create Date: 2023-04-24 23:18:51.644687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2782e433a3a7'
down_revision = 'ee65802a99c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass

def downgrade() -> None:
    op.drop_table('users')
    pass