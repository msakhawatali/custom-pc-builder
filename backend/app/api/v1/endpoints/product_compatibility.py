from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductCompatibility
from app.schemas import (
    ProductCompatibilityCreate,
    ProductCompatibilityUpdate,
    ProductCompatibilityRead,
)

router = APIRouter(prefix="/product-compatibilities", tags=["Product Compatibilities"])


@router.post("", response_model=ProductCompatibilityRead, status_code=status.HTTP_201_CREATED)
def create_product_compatibility(payload: ProductCompatibilityCreate, db: Session = Depends(get_db)):
    compatibility = ProductCompatibility(**payload.model_dump())
    db.add(compatibility)
    db.commit()
    db.refresh(compatibility)
    return compatibility


@router.get("", response_model=list[ProductCompatibilityRead])
def list_product_compatibilities(db: Session = Depends(get_db)):
    return db.query(ProductCompatibility).all()


@router.get("/{compatibility_id}", response_model=ProductCompatibilityRead)
def get_product_compatibility(compatibility_id: int, db: Session = Depends(get_db)):
    compatibility = db.query(ProductCompatibility).filter(ProductCompatibility.id == compatibility_id).first()
    if compatibility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product compatibility not found")
    return compatibility


@router.patch("/{compatibility_id}", response_model=ProductCompatibilityRead)
def update_product_compatibility(
    compatibility_id: int, payload: ProductCompatibilityUpdate, db: Session = Depends(get_db)
):
    compatibility = db.query(ProductCompatibility).filter(ProductCompatibility.id == compatibility_id).first()
    if compatibility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product compatibility not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(compatibility, field, value)

    db.commit()
    db.refresh(compatibility)
    return compatibility


@router.delete("/{compatibility_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_compatibility(compatibility_id: int, db: Session = Depends(get_db)):
    compatibility = db.query(ProductCompatibility).filter(ProductCompatibility.id == compatibility_id).first()
    if compatibility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product compatibility not found")

    db.delete(compatibility)
    db.commit()