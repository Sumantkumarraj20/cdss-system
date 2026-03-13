from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .diagnosis import Diagnosis


class DrugDisease(Base):
    __tablename__ = "drug_disease"
    __table_args__ = (
        UniqueConstraint("drug_id", "disease_id", name="uq_drug_disease"),
        Index("ix_drug_disease_drug_id", "drug_id"),
        Index("ix_drug_disease_disease_id", "disease_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    disease_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diagnoses.id", ondelete="CASCADE"),
        nullable=False,
    )

    drug: Mapped["Drug"] = relationship("Drug", back_populates="diseases")
    disease: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="drugs")
