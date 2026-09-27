from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductVariant
from app.schemas import (
    ProductVariantCreate,
    ProductVariantUpdate,
    ProductVariantRead,
)

router = APIRouter(prefix="/product-variants", tags=["Product Variants"])


@router.post("", response_model=ProductVariantRead, status_code=status.HTTP_201_CREATED)
def create_product_variant(payload: ProductVariantCreate, db: Session = Depends(get_db)):
    variant = ProductVariant(**payload.model_dump())
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant


@router.get("", response_model=list[ProductVariantRead])
def list_product_variants(db: Session = Depends(get_db)):
    return db.query(ProductVariant).all()


@router.get("/{variant_id}", response_model=ProductVariantRead)
def get_product_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")
    return variant


@router.patch("/{variant_id}", response_model=ProductVariantRead)
def update_product_variant(variant_id: int, payload: ProductVariantUpdate, db: Session = Depends(get_db)):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(variant, field, value)

    db.commit()
    db.refresh(variant)
    return variant


@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")

    db.delete(variant)
    db.commit()