from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .side_effect import SideEffect


class DrugSideEffect(Base):
    __tablename__ = "drug_side_effect"
    __table_args__ = (
        UniqueConstraint("drug_id", "side_effect_id", name="uq_drug_side_effect"),
        Index("ix_drug_side_effect_drug_id", "drug_id"),
        Index("ix_drug_side_effect_side_effect_id", "side_effect_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    side_effect_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("side_effects.id", ondelete="CASCADE"),
        nullable=False,
    )
    frequency: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    drug: Mapped["Drug"] = relationship("Drug", back_populates="side_effects")
    side_effect: Mapped["SideEffect"] = relationship(
        "SideEffect", back_populates="drugs"
    )
