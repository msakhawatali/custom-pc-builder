from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from app.db.base import Base


class SavedBuildItem(Base):
    __tablename__ = "saved_build_items"

    id = Column(Integer, primary_key=True, index=True)
    saved_build_id = Column(Integer, ForeignKey("saved_builds.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())