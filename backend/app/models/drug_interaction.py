from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .mechanism import Mechanism


class DrugInteraction(Base):
    __tablename__ = "drug_interactions"
    __table_args__ = (
        UniqueConstraint("drug_a_id", "drug_b_id", name="uq_drug_interaction_pair"),
        Index("ix_drug_interaction_drug_a_id", "drug_a_id"),
        Index("ix_drug_interaction_drug_b_id", "drug_b_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_a_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    drug_b_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    severity: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mechanism: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    clinical_effect: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mechanism_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("mechanisms.id", ondelete="SET NULL"),
        nullable=True,
    )

    drug_a: Mapped["Drug"] = relationship(
        "Drug", foreign_keys=[drug_a_id], back_populates="interactions_primary"
    )
    drug_b: Mapped["Drug"] = relationship(
        "Drug", foreign_keys=[drug_b_id], back_populates="interactions_secondary"
    )
    mechanism_ref: Mapped[Optional["Mechanism"]] = relationship(
        "Mechanism", back_populates="interactions"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DrugInteraction {self.drug_a_id}->{self.drug_b_id} severity={self.severity}>"
