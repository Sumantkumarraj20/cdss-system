from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .drug import Drug


class DrugSubstitute(Base):
    __tablename__ = "drug_substitutes"
    __table_args__ = (
        UniqueConstraint("drug_id", "substitute_name", name="uq_drug_substitute"),
        Index("ix_drug_substitute_drug_id", "drug_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    substitute_name: Mapped[str] = mapped_column(String, nullable=False)

    drug: Mapped["Drug"] = relationship("Drug", back_populates="substitutes")
