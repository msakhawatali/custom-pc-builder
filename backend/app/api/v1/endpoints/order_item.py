from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import OrderItem
from app.schemas import OrderItemCreate, OrderItemUpdate, OrderItemRead

router = APIRouter(prefix="/order-items", tags=["Order Items"])


@router.post("", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED)
def create_order_item(payload: OrderItemCreate, db: Session = Depends(get_db)):
    item = OrderItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[OrderItemRead])
def list_order_items(db: Session = Depends(get_db)):
    return db.query(OrderItem).all()


@router.get("/{order_item_id}", response_model=OrderItemRead)
def get_order_item(order_item_id: int, db: Session = Depends(get_db)):
    item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return item


@router.patch("/{order_item_id}", response_model=OrderItemRead)
def update_order_item(order_item_id: int, payload: OrderItemUpdate, db: Session = Depends(get_db)):
    item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")

    db.delete(item)
    db.commit()