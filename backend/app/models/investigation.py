from __future__ import annotations

import uuid
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .diagnosis_investigation import DiagnosisInvestigation


class Investigation(Base):
    __tablename__ = "investigations"
    __table_args__ = (
        UniqueConstraint("name", name="uq_investigations_name"),
        Index("idx_investigation_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    diagnoses: Mapped[List["DiagnosisInvestigation"]] = relationship(
        "DiagnosisInvestigation", back_populates="investigation", cascade="all, delete-orphan"
    )
