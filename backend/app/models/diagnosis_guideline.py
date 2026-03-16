from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .diagnosis import Diagnosis
    from .guideline import Guideline


class DiagnosisGuideline(Base):
    __tablename__ = "diagnosis_guidelines"
    __table_args__ = (
        UniqueConstraint("diagnosis_id", "guideline_id", name="uq_diagnosis_guideline"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnosis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id", ondelete="CASCADE"))
    guideline_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("guidelines.id", ondelete="CASCADE"))
    recommendation: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="guidelines")
    guideline: Mapped["Guideline"] = relationship("Guideline", back_populates="diagnoses")
