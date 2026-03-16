from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .lab_test import LabTest


class DrugLabEffect(Base):
    __tablename__ = "drug_lab_effect"
    __table_args__ = (
        UniqueConstraint("drug_id", "lab_test_id", name="uq_drug_lab_effect"),
        Index("ix_drug_lab_effect_drug_id", "drug_id"),
        Index("ix_drug_lab_effect_lab_test_id", "lab_test_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    lab_test_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lab_tests.id", ondelete="CASCADE"),
        nullable=False,
    )
    effect: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    drug: Mapped["Drug"] = relationship("Drug", back_populates="lab_effects")
    lab_test: Mapped["LabTest"] = relationship("LabTest", back_populates="drug_effects")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DrugLabEffect drug={self.drug_id} lab={self.lab_test_id}>"
