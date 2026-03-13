from __future__ import annotations

import uuid
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .drug_lab_effect import DrugLabEffect


class LabTest(Base):
    __tablename__ = "lab_tests"
    __table_args__ = (
        UniqueConstraint("name", name="uq_lab_tests_name"),
        Index("ix_lab_tests_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    drug_effects: Mapped[List["DrugLabEffect"]] = relationship(
        "DrugLabEffect", back_populates="lab_test", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<LabTest {self.name}>"
