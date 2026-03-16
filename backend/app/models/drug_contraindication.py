from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .diagnosis import Diagnosis


class DrugContraindication(Base):
    __tablename__ = "drug_contraindication"
    __table_args__ = (
        UniqueConstraint("drug_id", "condition_id", name="uq_drug_contraindication"),
        Index("ix_drug_contraindication_drug_id", "drug_id"),
        Index("ix_drug_contraindication_condition_id", "condition_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    condition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diagnoses.id", ondelete="CASCADE"),
        nullable=False,
    )
    severity: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    drug: Mapped["Drug"] = relationship("Drug", back_populates="contraindications")
    condition: Mapped["Diagnosis"] = relationship("Diagnosis")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DrugContraindication drug={self.drug_id} condition={self.condition_id}>"
