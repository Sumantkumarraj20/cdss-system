from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .drug import Drug


class DrugDosing(Base):
    __tablename__ = "drug_dosing"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drug_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drugs.id", ondelete="CASCADE"))
    adult_dose: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pediatric_dose: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    renal_adjustment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    drug: Mapped["Drug"] = relationship("Drug", back_populates="dosing")
