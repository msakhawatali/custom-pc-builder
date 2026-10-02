from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import CartItem
from app.schemas import CartItemCreate, CartItemUpdate, CartItemRead

router = APIRouter(prefix="/cart-items", tags=["Cart Items"])


@router.post("", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
def create_cart_item(payload: CartItemCreate, db: Session = Depends(get_db)):
    item = CartItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[CartItemRead])
def list_cart_items(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@router.get("/{cart_item_id}", response_model=CartItemRead)
def get_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return item


@router.patch("/{cart_item_id}", response_model=CartItemRead)
def update_cart_item(cart_item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    db.delete(item)
    db.commit()