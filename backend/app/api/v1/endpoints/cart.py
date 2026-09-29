from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import Cart
from app.schemas import CartCreate, CartUpdate, CartRead

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def create_cart(payload: CartCreate, db: Session = Depends(get_db)):
    cart = Cart(**payload.model_dump())
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


@router.get("", response_model=list[CartRead])
def list_carts(db: Session = Depends(get_db)):
    return db.query(Cart).all()


@router.get("/{cart_id}", response_model=CartRead)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return cart


@router.patch("/{cart_id}", response_model=CartRead)
def update_cart(cart_id: int, payload: CartUpdate, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cart, field, value)

    db.commit()
    db.refresh(cart)
    return cart


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    db.delete(cart)
    db.commit()