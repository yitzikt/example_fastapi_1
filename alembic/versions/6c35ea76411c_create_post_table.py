"""create post table

Revision ID: 6c35ea76411c
Revises: 
Create Date: 2022-05-20 12:56:25.662758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c35ea76411c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('post')
    pass
