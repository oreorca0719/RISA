"""create users table

Revision ID: 001
Revises: 
Create Date: 2026-04-26
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('role', sa.Enum('student', 'parent', 'teacher', 'admin', name='userrole'), nullable=False),
        sa.Column('grade', sa.Enum('elem1', 'elem2', 'elem3', 'elem4', 'elem5', 'elem6', 'mid1', name='gradelevel'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_username', 'users', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS gradelevel')
