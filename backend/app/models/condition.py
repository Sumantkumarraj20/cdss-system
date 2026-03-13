# Compatibility shim: conditions are represented by the canonical Diagnosis model.
from app.models.diagnosis import Diagnosis as Condition  # type: ignore

__all__ = ["Condition"]
