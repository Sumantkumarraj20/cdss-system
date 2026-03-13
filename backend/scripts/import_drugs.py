import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.drug import Drug
from app.models.drug_substitute import DrugSubstitute
from app.models.side_effect import SideEffect
from app.models.disease import Disease
from app.models.drug_side_effect import DrugSideEffect
from app.models.drug_disease import DrugDisease


CSV_FILE = "all_medicine databased.csv"


def main():
    print("Loading CSV...")
    df = pd.read_csv(CSV_FILE, low_memory=False, dtype=str)

    db: Session = SessionLocal()

    # caches to avoid duplicate nodes and to reuse existing DB rows
    side_effect_cache: dict[str, uuid.UUID] = {}
    disease_cache: dict[str, uuid.UUID] = {}
    drug_cache: dict[str, uuid.UUID] = {
        name: id_
        for name, id_ in db.execute(select(Drug.name, Drug.id)).all()
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

        if name in drug_cache:
            drug_id = drug_cache[name]
        else:
            drug = Drug(
                name=name,
                generic_name=row.get("generic_name"),
                chemical_class=row.get("Chemical Class"),
                habit_forming=str(row.get("Habit Forming")).lower() == "yes",
                pregnancy_category=row.get("pregnancy_category"),
                lactation_safety=row.get("lactation_safety"),
            )
            db.add(drug)
            db.flush()
            drug_id = drug.id
            drug_cache[name] = drug_id

        # Drug Substitutes
        for col in substitute_cols:
            val = row.get(col)
            if pd.notna(val) and str(val).strip():
                db.merge(
                    DrugSubstitute(
                        drug_id=drug_id,
                        substitute_name=str(val).strip(),
                    )
                )

        # Side Effect Nodes + Edges
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

            db.merge(
                DrugSideEffect(
                    drug_id=drug_id,
                    side_effect_id=side_effect_cache[val],
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

            db.merge(
                DrugDisease(
                    drug_id=drug_id,
                    disease_id=disease_cache[val],
                )
            )

        if idx % 1000 == 0:
            db.commit()

    db.commit()
    db.close()

    print("Import completed successfully.")


if __name__ == "__main__":
    main()
