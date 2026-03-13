from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DecisionRule(Base):
    __tablename__ = "decision_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    logic: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
