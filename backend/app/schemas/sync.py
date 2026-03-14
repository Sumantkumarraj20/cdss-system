from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SyncPullRequest(BaseModel):
    checkpoint: Optional[Dict[str, Any]] = None
    limit: int = 50


class SyncPullResponse(BaseModel):
    documents: List[Dict[str, Any]]
    checkpoint: Optional[Dict[str, Any]] = None


class SyncPushRequest(BaseModel):
    documents: List[Dict[str, Any]] = []
