"""update user model columns

Revision ID: fb094c394748
Revises: 4c60a815b32e
Create Date: 2026-08-20 01:34:40.818026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb094c394748'
down_revision: Union[str, Sequence[str], None] = '4c60a815b32e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users',
        'full_name',
        new_column_name='name',
        existing_type=sa.String(length=255),
        nullable=False,
    )
    op.add_column('users', sa.Column('phone', sa.String(length=30), nullable=True))
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(length=20),
            server_default='user',
            nullable=False,
        ),
    )
    op.add_column(
        'users',
        sa.Column(
            'language',
            sa.String(length=5),
            server_default='en',
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'language')
    op.drop_column('users', 'role')
    op.drop_column('users', 'phone')
    op.alter_column(
        'users',
        'name',
        new_column_name='full_name',
        existing_type=sa.String(length=255),
        nullable=True,
    )
