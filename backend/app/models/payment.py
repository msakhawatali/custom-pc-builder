from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_method = Column(String, nullable=False)
    transaction_id = Column(String, nullable=True, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String, nullable=False, default="pending", index=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())