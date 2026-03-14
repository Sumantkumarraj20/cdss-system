from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.drug import (
    DrugDetail,
    DrugSearchResult,
    DrugCreate,
    DrugUpdate,
)
from app.services import drug_service

router = APIRouter(prefix="/drugs", tags=["drugs"])


@router.get("/search", response_model=DrugSearchResult)
def search_drugs(
    q: str = Query(..., min_length=2, description="Drug name or generic"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = drug_service.search_drugs(db, q, limit=limit, offset=offset)
    return DrugSearchResult(items=items, total=total)


@router.get("/{drug_id}", response_model=DrugDetail)
def get_drug(drug_id: UUID, db: Session = Depends(get_db)):
    drug = drug_service.get_drug(db, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")

    return DrugDetail(
        id=drug.id,
        name=drug.name,
        generic_name=drug.generic_name,
        chemical_class=drug.chemical_class,
        habit_forming=drug.habit_forming,
        pregnancy_category=drug.pregnancy_category,
        lactation_safety=drug.lactation_safety,
        therapeutic_class=drug.therapeutic_class,
        mechanism=drug.mechanism,
        side_effects=[dse.side_effect for dse in drug.side_effects],
        diseases=[dd.disease for dd in drug.diseases],
        contraindications=[dc.condition for dc in drug.contraindications],
    )


@router.post("", response_model=DrugDetail, status_code=201)
def create_drug(payload: DrugCreate = Body(...), db: Session = Depends(get_db)):
    drug = drug_service.create_drug(db, payload)
    return get_drug(drug.id, db)  # reuse existing serializer


@router.patch("/{drug_id}", response_model=DrugDetail)
def update_drug_endpoint(
    drug_id: UUID, payload: DrugUpdate = Body(...), db: Session = Depends(get_db)
):
    drug = drug_service.update_drug(db, drug_id, payload)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return get_drug(drug.id, db)
