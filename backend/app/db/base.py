"""SQLAlchemy declarative base for the CDSS knowledge graph models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AuditBase(DeclarativeBase):
    """Base class that injects audit + soft delete columns into every model."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        nullable=False,
    )


# Single source of truth for the metadata Base across the project
Base = AuditBase


__all__ = ["Base"]
