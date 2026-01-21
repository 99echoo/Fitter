"""Add clothing_items to try_on_request.

Revision ID: 20250210_try_on_items
Revises: None
Create Date: 2025-02-10 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20250210_try_on_items"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "try_on_request",
        sa.Column("clothing_items", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("try_on_request", "clothing_items")
