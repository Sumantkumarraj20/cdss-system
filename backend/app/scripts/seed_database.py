"""Seed the CDSS knowledge graph with structured JSON data.

Reads app/data/diagnoses.json and upserts core entities plus junctions.
Run: `python -m app.scripts.seed_database` (ensure DATABASE_URL / CDSS_DATABASE_URL set).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import (
    Diagnosis,
    Symptom,
    Sign,
    Presentation,
    RedFlag,
    Drug,
    DiagnosisDrug,
    DiagnosisSymptom,
    DiagnosisSign,
    Investigation,
    DiagnosisInvestigation,
    Intervention,
    DiagnosisIntervention,
    Guideline,
    DiagnosisGuideline,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DIAG_FILE = DATA_DIR / "diagnoses.json"


def get_or_create(session: Session, model, defaults: Optional[dict] = None, **kwargs):
    instance = session.scalar(select(model).filter_by(**kwargs))
    if instance:
        return instance
    params = {**(defaults or {}), **kwargs}
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance


def seed():
    if not DIAG_FILE.exists():
        raise FileNotFoundError(f"Seed file missing: {DIAG_FILE}")

    with DIAG_FILE.open() as f:
        payload = json.load(f)

    session = SessionLocal()
    try:
        for item in payload:
            diagnosis = get_or_create(
                session,
                Diagnosis,
                name=item["name"],
                defaults={
                    "icd10_code": item.get("icd10"),
                    "description": item.get("description"),
                },
            )

            # Symptoms
            for name in item.get("symptoms", []):
                sym = get_or_create(session, Symptom, name=name)
                get_or_create(
                    session,
                    DiagnosisSymptom,
                    diagnosis_id=diagnosis.id,
                    symptom_id=sym.id,
                )

            # Signs
            for name in item.get("signs", []):
                sign = get_or_create(session, Sign, name=name)
                get_or_create(
                    session,
                    DiagnosisSign,
                    diagnosis_id=diagnosis.id,
                    sign_id=sign.id,
                )

            # Investigations
            for name in item.get("investigations", []):
                inv = get_or_create(session, Investigation, name=name)
                get_or_create(
                    session,
                    DiagnosisInvestigation,
                    diagnosis_id=diagnosis.id,
                    investigation_id=inv.id,
                )

            # Interventions
            for name in item.get("interventions", []):
                intervention = get_or_create(session, Intervention, name=name)
                get_or_create(
                    session,
                    DiagnosisIntervention,
                    diagnosis_id=diagnosis.id,
                    intervention_id=intervention.id,
                )

            # Drugs
            for name in item.get("drugs", []):
                drug = get_or_create(session, Drug, name=name, defaults={"generic_name": name})
                get_or_create(
                    session,
                    DiagnosisDrug,
                    diagnosis_id=diagnosis.id,
                    drug_id=drug.id,
                )

            # Guidelines
            for g in item.get("guidelines", []):
                guideline = get_or_create(
                    session,
                    Guideline,
                    title=g.get("title"),
                    organization=g.get("organization"),
                    publication_year=g.get("publication_year"),
                )
                get_or_create(
                    session,
                    DiagnosisGuideline,
                    diagnosis_id=diagnosis.id,
                    guideline_id=guideline.id,
                    defaults={"recommendation": g.get("recommendation")},
                )

            # Red flags tied to presentation if available, else to diagnosis description text
            for text in item.get("red_flags", []):
                # attach to a generic presentation named after first symptom or diagnosis
                pres_name = (item.get("presentations") or item.get("symptoms") or [item["name"]])[0]
                presentation = get_or_create(session, Presentation, name=pres_name)
                get_or_create(
                    session,
                    RedFlag,
                    presentation_id=presentation.id,
                    description=text,
                )

        session.commit()
        print(f"Seeded {len(payload)} diagnoses and related entities.")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
