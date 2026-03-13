from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.clinical import (
    DrugsResponse,
    DrugInteractionsResponse,
    PresentationBundle,
    DecisionSupportRequest,
    DecisionSupportResponse,
    SearchResult,
)
from app.schemas.drug import DrugBase
from app.services import clinical_query_service

router = APIRouter(prefix="/clinical", tags=["clinical"])


@router.get("/drugs-by-side-effect", response_model=DrugsResponse)
def drugs_by_side_effect(
    name: str = Query(..., description="Side effect name"),
    db: Session = Depends(get_db),
):
    items = clinical_query_service.find_drugs_causing_side_effect(db, name)
    return DrugsResponse(items=items)


@router.get("/drugs-by-disease", response_model=DrugsResponse)
def drugs_by_disease(
    name: str = Query(..., description="Disease/indication name"),
    db: Session = Depends(get_db),
):
    items = clinical_query_service.find_drugs_for_disease(db, name)
    return DrugsResponse(items=items)


@router.get("/drug-contraindications", response_model=DrugsResponse)
def drugs_contraindicated(
    condition: str = Query(..., description="Condition name, e.g., Pregnancy"),
    db: Session = Depends(get_db),
):
    items = clinical_query_service.find_drugs_contraindicated_in(db, condition)
    return DrugsResponse(items=items)


@router.get("/drug-interactions", response_model=DrugsResponse)
def drug_interactions(
    drug: str = Query(..., description="Drug name to check interactions for"),
    db: Session = Depends(get_db),
):
    items = clinical_query_service.find_drug_interactions(db, drug)
    return DrugsResponse(items=items)


@router.get("/drugs-by-ecg-effect", response_model=DrugsResponse)
def drugs_by_ecg_effect(
    effect: str = Query(..., description="ECG effect, e.g., QT prolongation"),
    db: Session = Depends(get_db),
):
    items = clinical_query_service.find_drugs_causing_ecg_effect(db, effect)
    return DrugsResponse(items=items)


@router.get("/presentations/{name}", response_model=PresentationBundle)
def presentation_bundle(name: str, db: Session = Depends(get_db)):
    bundle = clinical_query_service.get_presentation_bundle(db, name)
    if not bundle:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return bundle


@router.post("/decision-support", response_model=DecisionSupportResponse)
def decision_support(payload: DecisionSupportRequest = Body(...), db: Session = Depends(get_db)):
    result = clinical_query_service.run_decision_support(
        db,
        symptoms=payload.symptoms,
        signs=payload.signs,
        vitals=payload.vitals or {},
    )
    return DecisionSupportResponse(**result)


@router.get("/search", response_model=list[SearchResult])
def clinical_search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return clinical_query_service.search_entities(db, q)
