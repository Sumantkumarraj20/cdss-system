# Compatibility shim: diseases are now represented by the canonical Diagnosis model.
# Importing Disease yields the Diagnosis mapped class.
from app.models.diagnosis import Diagnosis as Disease  # type: ignore

__all__ = ["Disease"]
