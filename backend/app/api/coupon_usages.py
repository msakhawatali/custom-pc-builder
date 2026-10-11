from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import CouponUsage
from app.schemas import CouponUsageCreate, CouponUsageUpdate, CouponUsageRead

router = APIRouter(prefix="/coupon-usages", tags=["Coupon Usages"])


@router.post("", response_model=CouponUsageRead, status_code=status.HTTP_201_CREATED)
def create_coupon_usage(user_id: int, payload: CouponUsageCreate, db: Session = Depends(get_db)):
    usage = CouponUsage(**payload.model_dump(), user_id=user_id)
    db.add(usage)
    db.commit()
    db.refresh(usage)
    return usage


@router.get("", response_model=list[CouponUsageRead])
def list_coupon_usages(db: Session = Depends(get_db)):
    return db.query(CouponUsage).all()


@router.get("/{usage_id}", response_model=CouponUsageRead)
def get_coupon_usage(usage_id: int, db: Session = Depends(get_db)):
    usage = db.query(CouponUsage).filter(CouponUsage.id == usage_id).first()
    if usage is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon usage not found")
    return usage


@router.put("/{usage_id}", response_model=CouponUsageRead)
def update_coupon_usage(usage_id: int, payload: CouponUsageUpdate, db: Session = Depends(get_db)):
    usage = db.query(CouponUsage).filter(CouponUsage.id == usage_id).first()
    if usage is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon usage not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(usage, field, value)

    db.commit()
    db.refresh(usage)
    return usage


@router.delete("/{usage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon_usage(usage_id: int, db: Session = Depends(get_db)):
    usage = db.query(CouponUsage).filter(CouponUsage.id == usage_id).first()
    if usage is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon usage not found")

    db.delete(usage)
    db.commit()