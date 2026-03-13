from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .diagnosis import Diagnosis
    from .drug import Drug


class DiagnosisDrug(Base):
    __tablename__ = "diagnosis_drugs"
    __table_args__ = (
        UniqueConstraint("diagnosis_id", "drug_id", name="uq_diagnosis_drug"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnosis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id", ondelete="CASCADE"))
    drug_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drugs.id", ondelete="CASCADE"))
    indication_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    clinical_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="drugs")
    drug: Mapped["Drug"] = relationship("Drug", back_populates="diagnoses")
