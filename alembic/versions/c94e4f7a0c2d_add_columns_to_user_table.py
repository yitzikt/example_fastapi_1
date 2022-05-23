"""add columns to user table

Revision ID: c94e4f7a0c2d
Revises: f669625b0177
Create Date: 2022-05-20 13:36:47.626541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c94e4f7a0c2d'
down_revision = 'f669625b0177'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('publish', sa.Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'publish')
    pass
