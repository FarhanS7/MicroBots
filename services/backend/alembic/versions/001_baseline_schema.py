"""baseline schema for workspaces, actors, and task_records

Revision ID: 001_baseline_schema
Revises:
Create Date: 2026-09-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '001_baseline_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'workspaces',
        sa.Column('id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('owner_id', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workspaces_owner_id'), 'workspaces', ['owner_id'], unique=False)

    op.create_table(
        'actors',
        sa.Column('id', sa.String(length=64), nullable=False),
        sa.Column('workspace_id', sa.String(length=64), nullable=False),
        sa.Column('role', sa.String(length=32), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actors_workspace_id'), 'actors', ['workspace_id'], unique=False)

    op.create_table(
        'task_records',
        sa.Column('id', sa.String(length=64), nullable=False),
        sa.Column('workspace_id', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('payload_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_records_workspace_id'), 'task_records', ['workspace_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_task_records_workspace_id'), table_name='task_records')
    op.drop_table('task_records')
    op.drop_index(op.f('ix_actors_workspace_id'), table_name='actors')
    op.drop_table('actors')
    op.drop_index(op.f('ix_workspaces_owner_id'), table_name='workspaces')
    op.drop_table('workspaces')
