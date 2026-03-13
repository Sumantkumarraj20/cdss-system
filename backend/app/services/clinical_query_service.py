from __future__ import annotations

from typing import List
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.drug import Drug
from app.models.side_effect import SideEffect
from app.models.disease import Disease
from app.models.condition import Condition
from app.models.ecg_effect import ECGEffect
from app.models.drug_side_effect import DrugSideEffect
from app.models.drug_disease import DrugDisease
from app.models.drug_contraindication import DrugContraindication
from app.models.drug_interaction import DrugInteraction
from app.models.drug_lab_effect import DrugLabEffect
from app.models.lab_test import LabTest
from app.models.drug_ecg_effect import DrugECGEffect
from app.models.presentation import Presentation
from app.models.presentation_diagnosis import PresentationDiagnosis
from app.models.red_flag import RedFlag
from app.models.diagnosis import Diagnosis
from app.models.investigation import Investigation
from app.models.diagnosis_investigation import DiagnosisInvestigation
from app.models.decision_rule import DecisionRule
from app.models.symptom import Symptom
from app.models.sign import Sign
from app.models.drug import Drug


def _normalize_name(name: str) -> str:
    return name.strip().lower()


def find_drugs_causing_side_effect(db: Session, side_effect_name: str) -> List[Drug]:
    stmt = (
        select(Drug)
        .join(DrugSideEffect, Drug.id == DrugSideEffect.drug_id)
        .join(SideEffect, DrugSideEffect.side_effect_id == SideEffect.id)
        .where(func.lower(SideEffect.name) == _normalize_name(side_effect_name))
        .order_by(Drug.name)
    )
    return db.scalars(stmt).all()


def find_drugs_for_disease(db: Session, disease_name: str) -> List[Drug]:
    stmt = (
        select(Drug)
        .join(DrugDisease, Drug.id == DrugDisease.drug_id)
        .join(Disease, DrugDisease.disease_id == Disease.id)
        .where(func.lower(Disease.name) == _normalize_name(disease_name))
        .order_by(Drug.name)
    )
    return db.scalars(stmt).all()


def find_drugs_contraindicated_in(db: Session, condition_name: str) -> List[Drug]:
    stmt = (
        select(Drug)
        .join(DrugContraindication, Drug.id == DrugContraindication.drug_id)
        .join(Condition, DrugContraindication.condition_id == Condition.id)
        .where(func.lower(Condition.name) == _normalize_name(condition_name))
        .order_by(Drug.name)
    )
    return db.scalars(stmt).all()


def find_drug_interactions(db: Session, drug_name: str) -> List[Drug]:
    """Return drugs that interact with the given drug (both directions)."""

    norm = _normalize_name(drug_name)
    drug_ids = db.scalars(
        select(Drug.id).where(func.lower(Drug.name) == norm)
    ).all()
    if not drug_ids:
        return []

    stmt = (
        select(Drug)
        .join(DrugInteraction, Drug.id == DrugInteraction.drug_b_id)
        .where(DrugInteraction.drug_a_id.in_(drug_ids))
        .union(
            select(Drug)
            .join(DrugInteraction, Drug.id == DrugInteraction.drug_a_id)
            .where(DrugInteraction.drug_b_id.in_(drug_ids))
        )
    )
    return db.scalars(stmt).all()


def find_drugs_causing_ecg_effect(db: Session, ecg_effect_name: str) -> List[Drug]:
    stmt = (
        select(Drug)
        .join(DrugECGEffect, Drug.id == DrugECGEffect.drug_id)
        .join(ECGEffect, DrugECGEffect.ecg_effect_id == ECGEffect.id)
        .where(func.lower(ECGEffect.name) == _normalize_name(ecg_effect_name))
        .order_by(Drug.name)
    )
    return db.scalars(stmt).all()


def find_drugs_affecting_lab(db: Session, lab_name: str) -> List[DrugLabEffect]:
    stmt = (
        select(DrugLabEffect)
        .join(LabTest, DrugLabEffect.lab_test_id == LabTest.id)
        .where(func.lower(LabTest.name) == _normalize_name(lab_name))
    )
    return db.scalars(stmt).all()


def get_presentation_bundle(db: Session, name: str):
    norm = _normalize_name(name)
    presentation = db.scalars(
        select(Presentation).where(func.lower(Presentation.name) == norm)
    ).first()
    if not presentation:
        return None

    red_flags = db.scalars(
        select(RedFlag.description)
        .where(RedFlag.presentation_id == presentation.id)
        .order_by(RedFlag.urgency_level.nulls_last())
    ).all()

    diffs = db.scalars(
        select(Diagnosis.name)
        .join(PresentationDiagnosis, PresentationDiagnosis.diagnosis_id == Diagnosis.id)
        .where(PresentationDiagnosis.presentation_id == presentation.id)
        .order_by(PresentationDiagnosis.likelihood_score.desc().nulls_last())
    ).all()

    investigations = db.scalars(
        select(Investigation.name)
        .join(DiagnosisInvestigation, DiagnosisInvestigation.investigation_id == Investigation.id)
        .join(PresentationDiagnosis, PresentationDiagnosis.diagnosis_id == DiagnosisInvestigation.diagnosis_id)
        .where(PresentationDiagnosis.presentation_id == presentation.id)
        .distinct()
        .order_by(Investigation.name)
    ).all()

    treatments = db.scalars(
        select(Drug.name)
        .join(DiagnosisDrug, DiagnosisDrug.drug_id == Drug.id)
        .join(PresentationDiagnosis, PresentationDiagnosis.diagnosis_id == DiagnosisDrug.diagnosis_id)
        .where(PresentationDiagnosis.presentation_id == presentation.id)
        .distinct()
        .order_by(Drug.name)
    ).all()

    return {
        "presentation": presentation.name,
        "red_flags": red_flags,
        "differentials": diffs,
        "investigations": investigations,
        "treatments": treatments,
    }


def run_decision_support(db: Session, symptoms: list[str], signs: list[str], vitals: dict | None = None):
    norm_sym = {_normalize_name(s) for s in symptoms}
    norm_sign = {_normalize_name(s) for s in signs}

    suggestions = []
    rules = db.scalars(select(DecisionRule)).all()
    for rule in rules:
        logic = rule.logic or {}
        conditions = logic.get("conditions", [])
        ok = True
        for cond in conditions:
            if "symptom" in cond and _normalize_name(cond["symptom"]) not in norm_sym:
                ok = False
                break
            if "sign" in cond and _normalize_name(cond["sign"]) not in norm_sign:
                ok = False
                break
            if "vital" in cond and vitals:
                key = cond.get("vital")
                op = cond.get("op")
                val = cond.get("value")
                if key not in vitals:
                    ok = False
                    break
                try:
                    cur = float(vitals[key])
                    target = float(val)
                except Exception:
                    ok = False
                    break
                if op == ">" and not (cur > target):
                    ok = False
                    break
                if op == "<" and not (cur < target):
                    ok = False
                    break
        if ok and logic.get("suggest"):
            suggestions.append(logic["suggest"])

    # quick differential ranking: match diagnoses by symptom/sign overlap
    diag_scores = {}
    diag_sym = db.execute(
        select(Diagnosis.id, Diagnosis.name, Symptom.name)
        .join(DiagnosisSymptom, DiagnosisSymptom.diagnosis_id == Diagnosis.id)
        .join(Symptom, DiagnosisSymptom.symptom_id == Symptom.id)
    ).all()
    for did, dname, sname in diag_sym:
        if _normalize_name(sname) in norm_sym:
            diag_scores.setdefault(dname, 0)
            diag_scores[dname] += 1

    ranked = sorted(diag_scores.items(), key=lambda x: x[1], reverse=True)
    ranked_names = [name for name, _ in ranked][:10]

    return {
        "suggestions": suggestions,
        "ranked_differentials": ranked_names,
    }


def search_entities(db: Session, query: str, limit: int = 20):
    like = f"%{query.lower()}%"
    results = []
    for model, label in (
        (Presentation, "presentation"),
        (Diagnosis, "diagnosis"),
        (Symptom, "symptom"),
        (Drug, "drug"),
    ):
        rows = db.scalars(
            select(model).where(func.lower(model.name).like(like)).limit(limit)
        ).all()
        for r in rows:
            results.append({"type": label, "name": r.name})
    return results[:limit]
