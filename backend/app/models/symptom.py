from __future__ import annotations

import uuid
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .diagnosis_symptom import DiagnosisSymptom


class Symptom(Base):
    __tablename__ = "symptoms"
    __table_args__ = (
        UniqueConstraint("name", name="uq_symptoms_name"),
        Index("idx_symptom_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    diagnoses: Mapped[List["DiagnosisSymptom"]] = relationship(
        "DiagnosisSymptom", back_populates="symptom", cascade="all, delete-orphan"
    )
