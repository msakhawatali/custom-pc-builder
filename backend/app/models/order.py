from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_number = Column(String, unique=True, nullable=False, index=True)
    status = Column(String, nullable=False, default="pending", index=True)
    payment_status = Column(String, nullable=False, default="pending", index=True)

    subtotal = Column(Numeric(12, 2), nullable=False)
    shipping_cost = Column(Numeric(12, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(12, 2), nullable=False, default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)

    shipping_full_name = Column(String, nullable=False)
    shipping_phone = Column(String, nullable=False)
    shipping_address = Column(String, nullable=False)
    shipping_city = Column(String, nullable=False)
    shipping_state = Column(String, nullable=True)
    shipping_postal_code = Column(String, nullable=True)
    shipping_country = Column(String, nullable=False)

    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())