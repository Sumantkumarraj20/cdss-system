from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .diagnosis import Diagnosis
    from .investigation import Investigation


class DiagnosisInvestigation(Base):
    __tablename__ = "diagnosis_investigations"
    __table_args__ = (
        UniqueConstraint("diagnosis_id", "investigation_id", name="uq_diagnosis_investigation"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnosis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id", ondelete="CASCADE"))
    investigation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"))
    purpose: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="investigations")
    investigation: Mapped["Investigation"] = relationship("Investigation", back_populates="diagnoses")
