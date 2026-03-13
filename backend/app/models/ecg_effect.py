from __future__ import annotations

import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .drug_ecg_effect import DrugECGEffect


class ECGEffect(Base):
    __tablename__ = "ecg_effects"
    __table_args__ = (
        UniqueConstraint("name", name="uq_ecg_effects_name"),
        Index("ix_ecg_effects_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    drug_effects: Mapped[List["DrugECGEffect"]] = relationship(
        "DrugECGEffect", back_populates="ecg_effect", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ECGEffect {self.name}>"
