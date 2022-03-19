"""add user table

Revision ID: 62adb14eed6c
Revises: 662088a93b88
Create Date: 2022-03-18 21:17:52.866553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62adb14eed6c'
down_revision = '662088a93b88'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
