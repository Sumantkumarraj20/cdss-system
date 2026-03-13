from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TherapeuticClassRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class MechanismRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str] = None


class SideEffectRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    severity: Optional[str] = None


class DiseaseRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    icd10_code: Optional[str] = None


class ConditionRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category: Optional[str] = None


class DrugBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    generic_name: Optional[str] = None
    chemical_class: Optional[str] = None
    habit_forming: bool
    pregnancy_category: Optional[str] = None
    lactation_safety: Optional[str] = None


class DrugDetail(DrugBase):
    therapeutic_class: Optional[TherapeuticClassRef] = None
    mechanism: Optional[MechanismRef] = None
    side_effects: List[SideEffectRef] = []
    diseases: List[DiseaseRef] = []
    contraindications: List[ConditionRef] = []


class DrugSearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: List[DrugBase]
    total: int
