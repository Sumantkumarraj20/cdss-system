from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .diagnosis import Diagnosis
    from .sign import Sign


class DiagnosisSign(Base):
    __tablename__ = "diagnosis_signs"
    __table_args__ = (
        UniqueConstraint("diagnosis_id", "sign_id", name="uq_diagnosis_sign"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnosis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id", ondelete="CASCADE"))
    sign_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("signs.id", ondelete="CASCADE"))
    sensitivity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    specificity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="signs")
    sign: Mapped["Sign"] = relationship("Sign", back_populates="diagnoses")
