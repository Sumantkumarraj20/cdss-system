from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SideEffect(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    severity: Optional[str] = None
