from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import Coupon
from app.schemas import CouponCreate, CouponUpdate, CouponRead

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.post("", response_model=CouponRead, status_code=status.HTTP_201_CREATED)
def create_coupon(payload: CouponCreate, db: Session = Depends(get_db)):
    coupon = Coupon(**payload.model_dump())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.get("", response_model=list[CouponRead])
def list_coupons(db: Session = Depends(get_db)):
    return db.query(Coupon).all()


@router.get("/{coupon_id}", response_model=CouponRead)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if coupon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    return coupon


@router.put("/{coupon_id}", response_model=CouponRead)
def update_coupon(coupon_id: int, payload: CouponUpdate, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if coupon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(coupon, field, value)

    db.commit()
    db.refresh(coupon)
    return coupon


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if coupon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")

    db.delete(coupon)
    db.commit()