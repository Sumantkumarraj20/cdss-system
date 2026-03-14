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
from app.models.condition import Condition
from app.models.therapeutic_class import TherapeuticClass
from app.models.mechanism import Mechanism


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


def _get_or_create_named(db: Session, model, name: str):
    inst = db.scalar(select(model).where(func.lower(model.name) == name.lower()))
    if inst:
        return inst
    inst = model(name=name)
    db.add(inst)
    db.flush()
    return inst


def create_drug(db: Session, payload):
    tc_id = None
    mech_id = None
    if payload.therapeutic_class:
        tc = _get_or_create_named(db, TherapeuticClass, payload.therapeutic_class)
        tc_id = tc.id
    if payload.mechanism:
        mech = _get_or_create_named(db, Mechanism, payload.mechanism)
        mech_id = mech.id

    drug = Drug(
        name=payload.name,
        generic_name=payload.generic_name,
        chemical_class=payload.chemical_class,
        therapeutic_class_id=tc_id,
        mechanism_id=mech_id,
        habit_forming=payload.habit_forming,
        pregnancy_category=payload.pregnancy_category,
        lactation_safety=payload.lactation_safety,
    )
    db.add(drug)
    db.flush()

    for se in payload.side_effects or []:
        se_row = _get_or_create_named(db, SideEffect, se)
        db.merge(DrugSideEffect(drug_id=drug.id, side_effect_id=se_row.id))

    for dz in payload.diseases or []:
        disease_row = _get_or_create_named(db, Disease, dz)
        db.merge(DrugDisease(drug_id=drug.id, disease_id=disease_row.id))

    for cond in payload.contraindications or []:
        cond_row = _get_or_create_named(db, Condition, cond)
        db.merge(DrugContraindication(drug_id=drug.id, condition_id=cond_row.id))

    db.commit()
    db.refresh(drug)
    return drug


def update_drug(db: Session, drug_id: UUID, payload):
    drug = db.get(Drug, drug_id)
    if not drug:
        return None

    for field in [
        "name",
        "generic_name",
        "chemical_class",
        "habit_forming",
        "pregnancy_category",
        "lactation_safety",
    ]:
        val = getattr(payload, field)
        if val is not None:
            setattr(drug, field, val)

    if payload.therapeutic_class is not None:
        tc = _get_or_create_named(db, TherapeuticClass, payload.therapeutic_class)
        drug.therapeutic_class_id = tc.id
    if payload.mechanism is not None:
        mech = _get_or_create_named(db, Mechanism, payload.mechanism)
        drug.mechanism_id = mech.id

    if payload.side_effects is not None:
        db.query(DrugSideEffect).filter(DrugSideEffect.drug_id == drug.id).delete()
        for se in payload.side_effects:
            se_row = _get_or_create_named(db, SideEffect, se)
            db.merge(DrugSideEffect(drug_id=drug.id, side_effect_id=se_row.id))

    if payload.diseases is not None:
        db.query(DrugDisease).filter(DrugDisease.drug_id == drug.id).delete()
        for dz in payload.diseases:
            disease_row = _get_or_create_named(db, Disease, dz)
            db.merge(DrugDisease(drug_id=drug.id, disease_id=disease_row.id))

    if payload.contraindications is not None:
        db.query(DrugContraindication).filter(
            DrugContraindication.drug_id == drug.id
        ).delete()
        for cond in payload.contraindications:
            cond_row = _get_or_create_named(db, Condition, cond)
            db.merge(DrugContraindication(drug_id=drug.id, condition_id=cond_row.id))

    db.commit()
    db.refresh(drug)
    return drug
