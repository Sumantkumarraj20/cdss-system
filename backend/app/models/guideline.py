from __future__ import annotations

import uuid
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .diagnosis_guideline import DiagnosisGuideline


class Guideline(Base):
    __tablename__ = "guidelines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    diagnoses: Mapped[List["DiagnosisGuideline"]] = relationship(
        "DiagnosisGuideline", back_populates="guideline", cascade="all, delete-orphan"
    )
