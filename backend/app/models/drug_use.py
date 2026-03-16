import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DrugUse(Base):

    __tablename__ = "drug_uses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    drug_id = Column(UUID(as_uuid=True), ForeignKey("drugs.id", ondelete="CASCADE"))

    indication = Column(String, nullable=False)

    drug = relationship("Drug", back_populates="uses")
