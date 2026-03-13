"""SQLAlchemy declarative base for the CDSS knowledge graph models."""

from sqlalchemy.orm import declarative_base


# Single source of truth for the metadata Base across the project
Base = declarative_base()


__all__ = ["Base"]
