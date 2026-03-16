import os
import sys
import pandas as pd
import uuid
import logging
from tqdm import tqdm
from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

# Ensure package imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.drug import Drug
from app.models.drug_substitute import DrugSubstitute
from app.models.side_effect import SideEffect
from app.models.disease import Disease
from app.models.drug_side_effect import DrugSideEffect
from app.models.drug_disease import DrugDisease
from app.models.therapeutic_class import TherapeuticClass
from app.models.mechanism import Mechanism

# --- CONFIGURATION ---
CSV_FILE = "all_medicine_databased.csv" 
BATCH_SIZE = 2000  # Smaller batches are safer for Neon connection stability

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_engines():
    """Force ONLY Neon for this run."""
    neon_url = os.getenv("DATABASE_URL")
    if not neon_url:
        print("ERROR: DATABASE_URL not found!")
        return []
    return [create_engine(neon_url, pool_pre_ping=True)]

def clean(val):
    v = str(val).strip()
    return None if v.lower() in ['nan', 'na', 'none', '', 'nan'] else v

def fetch_existing_mappings(engine):
    """Fetches existing name->id mappings to prevent ForeignKey/Constraint errors."""
    mappings = {
        'drug': {}, 'side_effect': {}, 'disease': {}, 
        'tc': {}, 'mech': {}
    }
    Session = sessionmaker(bind=engine)
    with Session() as session:
        logger.info(f"Loading existing cache from {engine.url.host}...")
        mappings['drug'] = {n: i for n, i in session.execute(select(Drug.name, Drug.id)).all()}
        mappings['side_effect'] = {n: i for n, i in session.execute(select(SideEffect.name, SideEffect.id)).all()}
        mappings['disease'] = {n: i for n, i in session.execute(select(Disease.name, Disease.id)).all()}
        mappings['tc'] = {n: i for n, i in session.execute(select(TherapeuticClass.name, TherapeuticClass.id)).all()}
        mappings['mech'] = {n: i for n, i in session.execute(select(Mechanism.name, Mechanism.id)).all()}
    return mappings

def run_sync():
    engines = get_engines()
    if not engines:
        logger.error("No database engines found. Check your environment variables.")
        return

    # Pass 0: Initial Cache from the primary engine (Local)
    # This ensures consistency: once an ID is assigned, it stays that way.
    master_cache = fetch_existing_mappings(engines[0])

    logger.info("Reading CSV...")
    df = pd.read_csv(CSV_FILE, low_memory=False)
    
    sub_cols = [c for c in df.columns if c.startswith("substitute")]
    se_cols = [c for c in df.columns if c.startswith("sideEffect")]
    use_cols = [c for c in df.columns if c.startswith("use")]

    # --- PHASE 1: PRE-CALCULATE NEW ENTITIES ---
    to_insert = {
        TherapeuticClass: [], Mechanism: [], SideEffect: [], Disease: [],
        Drug: [], DrugSubstitute: [], DrugSideEffect: [], DrugDisease: []
    }

    logger.info("Building Knowledge Graph structure in memory...")
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing Rows"):
        d_name = clean(row.get('name'))
        if not d_name: continue

        # Resolve TC and Mechanism
        tc_name = clean(row.get('Therapeutic Class'))
        if tc_name and tc_name not in master_cache['tc']:
            new_id = uuid.uuid4()
            master_cache['tc'][tc_name] = new_id
            to_insert[TherapeuticClass].append({"id": new_id, "name": tc_name})

        mech_name = clean(row.get('Action Class'))
        if mech_name and mech_name not in master_cache['mech']:
            new_id = uuid.uuid4()
            master_cache['mech'][mech_name] = new_id
            to_insert[Mechanism].append({"id": new_id, "name": mech_name})

        # Resolve Drug
        if d_name not in master_cache['drug']:
            d_id = uuid.uuid4()
            master_cache['drug'][d_name] = d_id
            to_insert[Drug].append({
                "id": d_id,
                "name": d_name,
                "generic_name": clean(row.get("generic_name")),
                "therapeutic_class_id": master_cache['tc'].get(tc_name),
                "mechanism_id": master_cache['mech'].get(mech_name),
                "habit_forming": str(row.get("Habit Forming")).lower() == "yes"
            })
        
        d_id = master_cache['drug'][d_name]

        # Resolve Side Effects
        for col in se_cols:
            val = clean(row.get(col))
            if val:
                if val not in master_cache['side_effect']:
                    se_id = uuid.uuid4()
                    master_cache['side_effect'][val] = se_id
                    to_insert[SideEffect].append({"id": se_id, "name": val})
                
                to_insert[DrugSideEffect].append({
                    "id": uuid.uuid4(), "drug_id": d_id, "side_effect_id": master_cache['side_effect'][val]
                })

        # Resolve Diseases
        for col in use_cols:
            val = clean(row.get(col))
            if val:
                if val not in master_cache['disease']:
                    dis_id = uuid.uuid4()
                    master_cache['disease'][val] = dis_id
                    to_insert[Disease].append({"id": dis_id, "name": val})
                
                to_insert[DrugDisease].append({
                    "id": uuid.uuid4(), "drug_id": d_id, "disease_id": master_cache['disease'][val]
                })

        # Substitutes
        for col in sub_cols:
            val = clean(row.get(col))
            if val:
                to_insert[DrugSubstitute].append({
                    "id": uuid.uuid4(), "drug_id": d_id, "substitute_name": val
                })

    # --- PHASE 2: SEQUENTIAL BULK INSERT ---
    # Order matters: Entities -> Parents -> Children
    insertion_order = [
        TherapeuticClass, Mechanism, SideEffect, Disease, 
        Drug, 
        DrugSubstitute, DrugSideEffect, DrugDisease
    ]

    for engine in engines:
        logger.info(f"Connecting to: {engine.url.host}")
        with engine.begin() as conn:
            for model in insertion_order:
                data = to_insert[model]
                if not data: continue
                
                logger.info(f"  Inserting {len(data)} rows into {model.__tablename__}...")
                for i in range(0, len(data), BATCH_SIZE):
                    chunk = data[i:i + BATCH_SIZE]
                    stmt = insert(model).values(chunk).on_conflict_do_nothing()
                    conn.execute(stmt)

if __name__ == "__main__":
    try:
        run_sync()
        logger.info("Knowledge Graph synchronization successful.")
    except Exception as e:
        logger.error(f"Sync failed: {e}")