from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import JSON, Index, String, Text, UniqueConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .presentation_diagnosis import PresentationDiagnosis
    from .diagnosis_symptom import DiagnosisSymptom
    from .diagnosis_sign import DiagnosisSign
    from .diagnosis_investigation import DiagnosisInvestigation
    from .diagnosis_intervention import DiagnosisIntervention
    from .diagnosis_guideline import DiagnosisGuideline
    from .diagnosis_drug import DiagnosisDrug
    from .drug_disease import DrugDisease


class Diagnosis(Base):
    __tablename__ = "diagnoses"
    __table_args__ = (
        UniqueConstraint("name", name="uq_diagnoses_name"),
        Index("idx_diag_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    icd10_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    epidemiology_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    high_yield_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    evidence_grade: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    presentations: Mapped[List["PresentationDiagnosis"]] = relationship(
        "PresentationDiagnosis", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    symptoms: Mapped[List["DiagnosisSymptom"]] = relationship(
        "DiagnosisSymptom", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    signs: Mapped[List["DiagnosisSign"]] = relationship(
        "DiagnosisSign", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    investigations: Mapped[List["DiagnosisInvestigation"]] = relationship(
        "DiagnosisInvestigation", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    interventions: Mapped[List["DiagnosisIntervention"]] = relationship(
        "DiagnosisIntervention", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    guidelines: Mapped[List["DiagnosisGuideline"]] = relationship(
        "DiagnosisGuideline", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    drugs: Mapped[List["DiagnosisDrug"]] = relationship(
        "DiagnosisDrug", back_populates="diagnosis", cascade="all, delete-orphan"
    )
    drug_diseases: Mapped[List["DrugDisease"]] = relationship(
        "DrugDisease", back_populates="disease", cascade="all, delete-orphan"
    )
