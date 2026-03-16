from __future__ import annotations

import uuid
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .diagnosis_sign import DiagnosisSign


class Sign(Base):
    __tablename__ = "signs"
    __table_args__ = (
        UniqueConstraint("name", name="uq_signs_name"),
        Index("idx_sign_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    diagnoses: Mapped[List["DiagnosisSign"]] = relationship(
        "DiagnosisSign", back_populates="sign", cascade="all, delete-orphan"
    )
