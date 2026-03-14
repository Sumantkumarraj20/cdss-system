"""add audit + soft delete columns across tables

Revision ID: 7e5eb96a5b73
Revises: bb421d6becc6
Create Date: 2026-03-13 10:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.db.base import Base
import app.models  # noqa: F401 - populate metadata tables


# revision identifiers, used by Alembic.
revision: str = "7e5eb96a5b73"
down_revision: Union[str, Sequence[str], None] = "617d2b6a8573"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAMES = sorted(Base.metadata.tables.keys())


def upgrade() -> None:
    """Add created_at, updated_at, is_deleted + supporting indexes."""

    for table in TABLE_NAMES:
        op.add_column(
            table,
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
        )
        op.add_column(
            table,
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
        )
        op.add_column(
            table,
            sa.Column(
                "is_deleted",
                sa.Boolean(),
                server_default=sa.false(),
                nullable=False,
            ),
        )
        op.create_index(
            f"ix_{table}_updated_at",
            table,
            ["updated_at"],
            unique=False,
        )
        op.create_index(
            f"ix_{table}_is_deleted",
            table,
            ["is_deleted"],
            unique=False,
        )


def downgrade() -> None:
    """Drop audit columns and indexes."""

    for table in TABLE_NAMES:
        op.drop_index(f"ix_{table}_is_deleted", table_name=table)
        op.drop_index(f"ix_{table}_updated_at", table_name=table)
        op.drop_column(table, "is_deleted")
        op.drop_column(table, "updated_at")
        op.drop_column(table, "created_at")
