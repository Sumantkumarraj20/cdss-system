from __future__ import annotations

import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .drug import Drug


class TherapeuticClass(Base):
    __tablename__ = "therapeutic_classes"
    __table_args__ = (
        UniqueConstraint("name", name="uq_therapeutic_class_name"),
        Index("ix_therapeutic_class_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    drugs: Mapped[List["Drug"]] = relationship(
        "Drug", back_populates="therapeutic_class"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<TherapeuticClass {self.name}>"
