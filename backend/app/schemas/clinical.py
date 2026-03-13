from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict

from .drug import DrugBase


class DrugsResponse(BaseModel):
    """Generic response wrapper for list of drugs."""

    model_config = ConfigDict(from_attributes=True)

    items: List[DrugBase]


class DrugInteractionsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    interacting_drugs: List[DrugBase]


class PresentationBundle(BaseModel):
    presentation: str
    red_flags: List[str]
    differentials: List[str]
    investigations: List[str]
    treatments: List[str]


class DecisionSupportRequest(BaseModel):
    symptoms: List[str] = []
    signs: List[str] = []
    vitals: dict | None = None


class DecisionSupportResponse(BaseModel):
    suggestions: List[str]
    ranked_differentials: List[str]


class SearchResult(BaseModel):
    type: str
    name: str
