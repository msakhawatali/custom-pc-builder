from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, func
from app.db.base import Base


class ProductReview(Base):
    __tablename__ = "product_reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())