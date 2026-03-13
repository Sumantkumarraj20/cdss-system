from __future__ import annotations

import uuid
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .therapeutic_class import TherapeuticClass
    from .mechanism import Mechanism
    from .drug_substitute import DrugSubstitute
    from .drug_side_effect import DrugSideEffect
    from .drug_disease import DrugDisease
    from .drug_contraindication import DrugContraindication
    from .drug_interaction import DrugInteraction
    from .drug_lab_effect import DrugLabEffect
    from .drug_ecg_effect import DrugECGEffect
    from .drug_use import DrugUse
    from .diagnosis_drug import DiagnosisDrug
    from .drug_dosing import DrugDosing
    from .diagnosis import Diagnosis


class Drug(Base):
    __tablename__ = "drugs"
    __table_args__ = (
        UniqueConstraint("name", name="uq_drugs_name"),
        UniqueConstraint("generic_name", name="uq_drugs_generic_name"),
        Index("ix_drugs_name", "name"),
        Index("ix_drugs_generic_name", "generic_name"),
        Index("ix_drugs_therapeutic_class_id", "therapeutic_class_id"),
        Index("ix_drugs_mechanism_id", "mechanism_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    generic_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    chemical_class: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    therapeutic_class_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("therapeutic_classes.id"), nullable=True
    )
    mechanism_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mechanisms.id"), nullable=True
    )
    habit_forming: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    pregnancy_category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lactation_safety: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    therapeutic_class: Mapped[Optional["TherapeuticClass"]] = relationship(
        "TherapeuticClass", back_populates="drugs"
    )
    mechanism: Mapped[Optional["Mechanism"]] = relationship(
        "Mechanism", back_populates="drugs"
    )
    substitutes: Mapped[List["DrugSubstitute"]] = relationship(
        "DrugSubstitute",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    side_effects: Mapped[List["DrugSideEffect"]] = relationship(
        "DrugSideEffect",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    diseases: Mapped[List["DrugDisease"]] = relationship(
        "DrugDisease",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    contraindications: Mapped[List["DrugContraindication"]] = relationship(
        "DrugContraindication",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    interactions_primary: Mapped[List["DrugInteraction"]] = relationship(
        "DrugInteraction",
        foreign_keys="DrugInteraction.drug_a_id",
        back_populates="drug_a",
        cascade="all, delete-orphan",
    )
    interactions_secondary: Mapped[List["DrugInteraction"]] = relationship(
        "DrugInteraction",
        foreign_keys="DrugInteraction.drug_b_id",
        back_populates="drug_b",
        cascade="all, delete-orphan",
    )
    lab_effects: Mapped[List["DrugLabEffect"]] = relationship(
        "DrugLabEffect",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    ecg_effects: Mapped[List["DrugECGEffect"]] = relationship(
        "DrugECGEffect",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    uses: Mapped[List["DrugUse"]] = relationship(
        "DrugUse",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    diagnoses: Mapped[List["DiagnosisDrug"]] = relationship(
        "DiagnosisDrug",
        back_populates="drug",
        cascade="all, delete-orphan",
    )
    dosing: Mapped[List["DrugDosing"]] = relationship(
        "DrugDosing",
        back_populates="drug",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover - helpful for debugging
        return f"<Drug {self.name} ({self.generic_name})>"
