"""add foreign key to post table

Revision ID: f669625b0177
Revises: 73642c1988d2
Create Date: 2022-05-20 13:17:33.947833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f669625b0177'
down_revision = '73642c1988d2'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('post', 'posts')
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    op.rename_table('posts', 'post')
    pass
