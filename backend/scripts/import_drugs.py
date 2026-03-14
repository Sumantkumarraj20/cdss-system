import sys
import os
import uuid

# Ensure package imports work when executed inside Docker or locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.models.drug import Drug
from app.models.drug_substitute import DrugSubstitute
from app.models.side_effect import SideEffect
from app.models.disease import Disease
from app.models.drug_side_effect import DrugSideEffect
from app.models.drug_disease import DrugDisease
from app.models.therapeutic_class import TherapeuticClass
from app.models.mechanism import Mechanism


CSV_FILE = "all_medicine databased.csv"


def main():
    print("Loading CSV...")
    df = pd.read_csv(CSV_FILE, low_memory=False, dtype=str)

    db_url = os.getenv(
        "DATABASE_URL",
        # Fallback to docker-compose service name to avoid localhost failures in containers.
        "postgresql+psycopg2://cdss:cdss@db:5432/cdss",
    )
    print(f"Connecting to DB: {db_url}")
    engine = create_engine(db_url, future=True)
    SessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )
    db: Session = SessionLocal()

    # caches to avoid duplicate nodes and to reuse existing DB rows
    side_effect_cache: dict[str, uuid.UUID] = {
        name: id_
        for name, id_ in db.execute(select(SideEffect.name, SideEffect.id)).all()
    }
    disease_cache: dict[str, uuid.UUID] = {
        name: id_
        for name, id_ in db.execute(select(Disease.name, Disease.id)).all()
    }
    therapeutic_cache: dict[str, uuid.UUID] = {
        name: id_
        for name, id_ in db.execute(
            select(TherapeuticClass.name, TherapeuticClass.id)
        ).all()
    }
    mechanism_cache: dict[str, uuid.UUID] = {
        name: id_
        for name, id_ in db.execute(select(Mechanism.name, Mechanism.id)).all()
    }
    drug_cache: dict[str, uuid.UUID] = {
        name: id_
        for name, id_ in db.execute(select(Drug.name, Drug.id)).all()
    }
    existing_substitutes = {
        (drug_id, name)
        for drug_id, name in db.execute(
            select(DrugSubstitute.drug_id, DrugSubstitute.substitute_name)
        ).all()
    }
    substitutes_seen = {}
    existing_drug_diseases = {
        (drug_id, disease_id)
        for drug_id, disease_id in db.execute(
            select(DrugDisease.drug_id, DrugDisease.disease_id)
        ).all()
    }
    existing_drug_side_effects = {
        (drug_id, se_id)
        for drug_id, se_id in db.execute(
            select(DrugSideEffect.drug_id, DrugSideEffect.side_effect_id)
        ).all()
    }

    # detect columns dynamically
    side_effect_cols = [c for c in df.columns if c.lower().startswith("sideeffect")]
    use_cols = [c for c in df.columns if c.lower().startswith("use")]
    substitute_cols = [c for c in df.columns if c.lower().startswith("substitute")]

    print(f"Side effect columns: {len(side_effect_cols)}")
    print(f"Use columns: {len(use_cols)}")
    print(f"Substitute columns: {len(substitute_cols)}")

    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"Processing {idx}/{len(df)}")

        name = str(row.get("name")).strip()
        if not name:
            continue

        # Therapeutic class & mechanism resolution (optional columns)
        therapeutic_name = str(row.get("Therapeutic Class") or "").strip()
        mechanism_name = str(row.get("Action Class") or "").strip()

        therapeutic_id = None
        if therapeutic_name:
            therapeutic_id = therapeutic_cache.get(therapeutic_name)
            if therapeutic_id is None:
                tc = TherapeuticClass(name=therapeutic_name)
                db.add(tc)
                db.flush()
                therapeutic_id = tc.id
                therapeutic_cache[therapeutic_name] = therapeutic_id

        mechanism_id = None
        if mechanism_name:
            mechanism_id = mechanism_cache.get(mechanism_name)
            if mechanism_id is None:
                mech = Mechanism(name=mechanism_name)
                db.add(mech)
                db.flush()
                mechanism_id = mech.id
                mechanism_cache[mechanism_name] = mechanism_id

        if name in drug_cache:
            drug_id = drug_cache[name]
        else:
            drug = Drug(
                name=name,
                generic_name=row.get("generic_name"),
                chemical_class=row.get("Chemical Class"),
                therapeutic_class_id=therapeutic_id,
                mechanism_id=mechanism_id,
                habit_forming=str(row.get("Habit Forming")).lower() == "yes",
                pregnancy_category=row.get("pregnancy_category"),
                lactation_safety=row.get("lactation_safety"),
            )
            db.add(drug)
            db.flush()
            drug_id = drug.id
            drug_cache[name] = drug_id

        # Drug Substitutes
        # Track seen substitutes per drug to avoid unique constraint violations
        per_drug_seen = substitutes_seen.setdefault(drug_id, set())
        for col in substitute_cols:
            val = row.get(col)
            if pd.notna(val) and str(val).strip():
                sub_name = str(val).strip()
                key = (drug_id, sub_name)
                if key in existing_substitutes or sub_name in per_drug_seen:
                    continue
                per_drug_seen.add(sub_name)
                existing_substitutes.add(key)
                db.add(
                    DrugSubstitute(
                        drug_id=drug_id,
                        substitute_name=sub_name,
                    )
                )

        # Side Effect Nodes + Edges
        # Side Effect Nodes + Edges (deduped)
        per_drug_side_seen = set()
        for col in side_effect_cols:
            val = row.get(col)
            if pd.isna(val):
                continue
            val = str(val).strip()
            if not val:
                continue

            if val not in side_effect_cache:
                se = SideEffect(name=val)
                db.add(se)
                db.flush()
                side_effect_cache[val] = se.id

            se_id = side_effect_cache[val]
            edge_key = (drug_id, se_id)
            if edge_key in existing_drug_side_effects or se_id in per_drug_side_seen:
                continue
            per_drug_side_seen.add(se_id)
            existing_drug_side_effects.add(edge_key)
            db.add(
                DrugSideEffect(
                    drug_id=drug_id,
                    side_effect_id=se_id,
                )
            )

        # Disease Nodes + Edges
        for col in use_cols:
            val = row.get(col)
            if pd.isna(val):
                continue
            val = str(val).strip()
            if not val:
                continue

            if val not in disease_cache:
                disease = Disease(name=val)
                db.add(disease)
                db.flush()
                disease_cache[val] = disease.id

            disease_id = disease_cache[val]
            edge_key = (drug_id, disease_id)
            if edge_key in existing_drug_diseases:
                continue
            existing_drug_diseases.add(edge_key)
            db.add(
                DrugDisease(
                    drug_id=drug_id,
                    disease_id=disease_id,
                )
            )

        if idx % 1000 == 0:
            db.commit()

    db.commit()
    db.close()

    print("Import completed successfully.")


if __name__ == "__main__":
    main()
