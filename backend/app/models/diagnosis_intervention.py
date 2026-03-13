from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .diagnosis import Diagnosis
    from .intervention import Intervention


class DiagnosisIntervention(Base):
    __tablename__ = "diagnosis_interventions"
    __table_args__ = (
        UniqueConstraint("diagnosis_id", "intervention_id", name="uq_diagnosis_intervention"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnosis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id", ondelete="CASCADE"))
    intervention_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("interventions.id", ondelete="CASCADE"))
    priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="interventions")
    intervention: Mapped["Intervention"] = relationship("Intervention", back_populates="diagnoses")
