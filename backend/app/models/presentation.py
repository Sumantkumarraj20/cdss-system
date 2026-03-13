from __future__ import annotations

import uuid
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .presentation_diagnosis import PresentationDiagnosis
    from .red_flag import RedFlag


class Presentation(Base):
    __tablename__ = "presentations"
    __table_args__ = (
        UniqueConstraint("name", name="uq_presentations_name"),
        Index("idx_pres_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    differentials: Mapped[List["PresentationDiagnosis"]] = relationship(
        "PresentationDiagnosis", back_populates="presentation", cascade="all, delete-orphan"
    )
    red_flags: Mapped[List["RedFlag"]] = relationship(
        "RedFlag", back_populates="presentation", cascade="all, delete-orphan"
    )
