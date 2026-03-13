from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .presentation import Presentation


class RedFlag(Base):
    __tablename__ = "red_flags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    presentation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("presentations.id", ondelete="CASCADE"))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    urgency_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    presentation: Mapped["Presentation"] = relationship("Presentation", back_populates="red_flags")
