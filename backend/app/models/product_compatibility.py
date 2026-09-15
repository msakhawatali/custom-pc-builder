from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.db.base import Base


class ProductCompatibility(Base):
    __tablename__ = "product_compatibilities"

    id = Column(Integer, primary_key=True, index=True)
    source_category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False, index=True)
    target_category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False, index=True)
    compatibility_key = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())