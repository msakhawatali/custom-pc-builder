from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from app.db.base import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    discount_type = Column(String, nullable=False)
    discount_value = Column(Numeric(12, 2), nullable=False)
    minimum_order_amount = Column(Numeric(12, 2), nullable=True)
    maximum_discount_amount = Column(Numeric(12, 2), nullable=True)
    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, nullable=False, default=0)
    starts_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())