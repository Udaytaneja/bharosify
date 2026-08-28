"""create documents table

Revision ID: e5a1b2c3d4e5
Revises: bcfaca1904c3
Create Date: 2026-08-29 01:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5a1b2c3d4e5'
down_revision: Union[str, Sequence[str], None] = 'bcfaca1904c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.String(length=36), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('stored_filename', sa.String(length=255), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('document_type', sa.String(length=50), nullable=False, server_default='Uploaded Document'),
        sa.Column('requirement', sa.String(length=20), nullable=False, server_default='REQUIRED'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='VERIFIED'),
        sa.Column('ocr_status', sa.String(length=30), nullable=False, server_default='COMPLETED'),
        sa.Column('ai_analysis', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_document_id'), 'documents', ['document_id'], unique=True)
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_index(op.f('ix_documents_owner_id'), 'documents', ['owner_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_documents_owner_id'), table_name='documents')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_index(op.f('ix_documents_document_id'), table_name='documents')
    op.drop_table('documents')
