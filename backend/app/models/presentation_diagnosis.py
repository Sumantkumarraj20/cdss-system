from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .presentation import Presentation
    from .diagnosis import Diagnosis


class PresentationDiagnosis(Base):
    __tablename__ = "presentation_diagnoses"
    __table_args__ = (
        UniqueConstraint("presentation_id", "diagnosis_id", name="uq_presentation_diagnosis"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    presentation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("presentations.id", ondelete="CASCADE"))
    diagnosis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id", ondelete="CASCADE"))
    likelihood_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    presentation: Mapped["Presentation"] = relationship("Presentation", back_populates="differentials")
    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="presentations")
