"""added content column to post table

Revision ID: 086f9fd7c3fa
Revises: 6c35ea76411c
Create Date: 2022-05-20 13:04:15.466894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '086f9fd7c3fa'
down_revision = '6c35ea76411c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("post", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('post', 'content')
    pass
