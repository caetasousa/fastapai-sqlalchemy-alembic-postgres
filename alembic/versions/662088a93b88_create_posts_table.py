"""create posts table

Revision ID: 662088a93b88
Revises: 
Create Date: 2022-03-18 20:54:45.355704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662088a93b88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass

def downgrade():
    op.drop_table('posts')
    pass
