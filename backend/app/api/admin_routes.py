from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.diagnosis import Diagnosis
from app.models.presentation import Presentation
from app.schemas.drug import DrugCreate, DrugDetail
from app.schemas.clinical import DiagnosisCreate, PresentationCreate
from app.services import drug_service
from app.core.auth import require_token

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_token)])


@router.post("/drugs", response_model=DrugDetail, status_code=201)
def admin_create_drug(payload: DrugCreate = Body(...), db: Session = Depends(get_db)):
    drug = drug_service.create_drug(db, payload)
    return drug_service.get_drug(db, drug.id)


@router.post("/diagnoses", response_model=UUID, status_code=201)
def admin_create_diagnosis(
    payload: DiagnosisCreate = Body(...), db: Session = Depends(get_db)
):
    diag = Diagnosis(
        name=payload.name,
        icd10_code=payload.icd10_code,
        description=payload.description,
    )
    db.add(diag)
    db.commit()
    return diag.id


@router.post("/presentations", response_model=UUID, status_code=201)
def admin_create_presentation(
    payload: PresentationCreate = Body(...), db: Session = Depends(get_db)
):
    pres = Presentation(name=payload.name, description=payload.description)
    db.add(pres)
    db.commit()
    return pres.id
