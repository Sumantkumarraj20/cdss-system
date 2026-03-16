from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .drug import Drug
    from .ecg_effect import ECGEffect


class DrugECGEffect(Base):
    __tablename__ = "drug_ecg_effect"
    __table_args__ = (
        UniqueConstraint("drug_id", "ecg_effect_id", name="uq_drug_ecg_effect"),
        Index("ix_drug_ecg_effect_drug_id", "drug_id"),
        Index("ix_drug_ecg_effect_ecg_effect_id", "ecg_effect_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drugs.id", ondelete="CASCADE"),
        nullable=False,
    )
    ecg_effect_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ecg_effects.id", ondelete="CASCADE"),
        nullable=False,
    )
    risk_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    drug: Mapped["Drug"] = relationship("Drug", back_populates="ecg_effects")
    ecg_effect: Mapped["ECGEffect"] = relationship(
        "ECGEffect", back_populates="drug_effects"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DrugECGEffect drug={self.drug_id} ecg={self.ecg_effect_id}>"
