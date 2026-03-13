from __future__ import annotations

import uuid
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .drug_interaction import DrugInteraction


class Mechanism(Base):
    __tablename__ = "mechanisms"
    __table_args__ = (
        UniqueConstraint("name", name="uq_mechanisms_name"),
        Index("ix_mechanisms_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    drugs: Mapped[List["Drug"]] = relationship("Drug", back_populates="mechanism")
    interactions: Mapped[List["DrugInteraction"]] = relationship(
        "DrugInteraction", back_populates="mechanism_ref"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Mechanism {self.name}>"
