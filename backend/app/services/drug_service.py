from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.drug import Drug
from app.models.drug_side_effect import DrugSideEffect
from app.models.drug_disease import DrugDisease
from app.models.drug_contraindication import DrugContraindication
from app.models.disease import Disease
from app.models.side_effect import SideEffect


def search_drugs(db: Session, query: str, limit: int = 20, offset: int = 0):
    """Full-text style search by drug name or generic name."""

    like = f"%{query.lower()}%"
    stmt = (
        select(Drug)
        .where(func.lower(Drug.name).like(like) | func.lower(Drug.generic_name).like(like))
        .order_by(Drug.name)
        .limit(limit)
        .offset(offset)
    )
    results = db.scalars(stmt).all()

    total = db.scalar(
        select(func.count())
        .select_from(Drug)
        .where(func.lower(Drug.name).like(like) | func.lower(Drug.generic_name).like(like))
    )

    return results, total


def get_drug(db: Session, drug_id: UUID) -> Optional[Drug]:
    """Fetch a single drug with relationships eagerly loaded where needed."""

    stmt = (
        select(Drug)
        .where(Drug.id == drug_id)
        .options(
            selectinload(Drug.therapeutic_class),
            selectinload(Drug.mechanism),
            selectinload(Drug.side_effects).selectinload(DrugSideEffect.side_effect),
            selectinload(Drug.diseases).selectinload(DrugDisease.disease),
            selectinload(Drug.contraindications).selectinload(
                DrugContraindication.condition
            ),
        )
    )
    return db.scalars(stmt).first()
