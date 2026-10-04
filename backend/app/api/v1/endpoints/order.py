import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import Order
from app.schemas import OrderCreate, OrderUpdate, OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])


def generate_order_number(db: Session) -> str:
    while True:
        candidate = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        exists = db.query(Order).filter(Order.order_number == candidate).first()
        if not exists:
            return candidate


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(user_id: int, payload: OrderCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    subtotal = data.pop("subtotal")
    shipping_cost = Decimal("0")
    discount_amount = Decimal("0")

    order = Order(
        **data,
        user_id=user_id,
        order_number=generate_order_number(db),
        subtotal=subtotal,
        total_amount=subtotal + shipping_cost - discount_amount,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, payload: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(order)
    db.commit()