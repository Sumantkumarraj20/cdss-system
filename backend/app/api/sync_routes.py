from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Tuple
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.drug import Drug
from app.models.diagnosis import Diagnosis
from app.models.presentation import Presentation
from app.schemas.sync import SyncPullRequest, SyncPullResponse, SyncPushRequest
from app.core.auth import require_token

router = APIRouter(prefix="/sync", tags=["sync"])


def _make_checkpoint(row) -> Dict[str, Any]:
    return {
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        "id": str(row.id),
    }


def _apply_checkpoint_filter(stmt, model, checkpoint: Dict[str, Any]):
    ts = checkpoint.get("updated_at")
    pk = checkpoint.get("id")
    if ts:
        try:
            dt = datetime.fromisoformat(ts)
            stmt = stmt.where(
                (model.updated_at > dt)
                | ((model.updated_at == dt) & (model.id > UUID(pk)))
            )
        except Exception:
            pass
    return stmt


def _serialize(row) -> Dict[str, Any]:
    data = {}
    for col in row.__table__.columns:
        val = getattr(row, col.key)
        if isinstance(val, datetime):
            data[col.key] = val.isoformat()
        elif isinstance(val, UUID):
            data[col.key] = str(val)
        else:
            data[col.key] = val
    return data


def _pull(model, req: SyncPullRequest, db: Session) -> SyncPullResponse:
    stmt = select(model).order_by(model.updated_at, model.id).limit(req.limit)
    if req.checkpoint:
        stmt = _apply_checkpoint_filter(stmt, model, req.checkpoint)
    rows = db.scalars(stmt).all()
    docs = [_serialize(r) for r in rows]
    checkpoint = _make_checkpoint(rows[-1]) if rows else req.checkpoint
    return SyncPullResponse(documents=docs, checkpoint=checkpoint)


def _push(model, docs, db: Session):
    for doc in docs:
        pk = doc.get("id")
        existing = db.get(model, UUID(pk)) if pk else None
        payload = {k: v for k, v in doc.items() if k in model.__table__.columns}
        if existing:
            for key, val in payload.items():
                setattr(existing, key, val)
        else:
            db.add(model(**payload))
    db.commit()


@router.post("/drugs", response_model=SyncPullResponse)
def sync_drugs(req: SyncPullRequest, db: Session = Depends(get_db)):
    return _pull(Drug, req, db)


@router.post("/drugs/push")
def sync_drugs_push(
    req: SyncPushRequest,
    db: Session = Depends(get_db),
    _: str = Depends(require_token),
):
    _push(Drug, req.documents, db)
    return {"status": "ok"}


@router.post("/diagnoses", response_model=SyncPullResponse)
def sync_diagnoses(req: SyncPullRequest, db: Session = Depends(get_db)):
    return _pull(Diagnosis, req, db)


@router.post("/diagnoses/push")
def sync_diagnoses_push(
    req: SyncPushRequest,
    db: Session = Depends(get_db),
    _: str = Depends(require_token),
):
    _push(Diagnosis, req.documents, db)
    return {"status": "ok"}


@router.post("/presentations", response_model=SyncPullResponse)
def sync_presentations(req: SyncPullRequest, db: Session = Depends(get_db)):
    return _pull(Presentation, req, db)


@router.post("/presentations/push")
def sync_presentations_push(
    req: SyncPushRequest,
    db: Session = Depends(get_db),
    _: str = Depends(require_token),
):
    _push(Presentation, req.documents, db)
    return {"status": "ok"}
