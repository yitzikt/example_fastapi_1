"""add user table

Revision ID: 73642c1988d2
Revises: 086f9fd7c3fa
Create Date: 2022-05-20 13:09:25.973832

"""
from http import server
from re import T
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73642c1988d2'
down_revision = '086f9fd7c3fa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
            server_default=sa.text('NOW()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
            )
    pass


def downgrade():
    op.drop_table('users')
    pass
