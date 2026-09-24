from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductSpecification
from app.schemas import (
    ProductSpecificationCreate,
    ProductSpecificationUpdate,
    ProductSpecificationRead,
)

router = APIRouter(prefix="/product-specifications", tags=["Product Specifications"])


@router.post("", response_model=ProductSpecificationRead, status_code=status.HTTP_201_CREATED)
def create_product_specification(payload: ProductSpecificationCreate, db: Session = Depends(get_db)):
    specification = ProductSpecification(**payload.model_dump())
    db.add(specification)
    db.commit()
    db.refresh(specification)
    return specification


@router.get("", response_model=list[ProductSpecificationRead])
def list_product_specifications(db: Session = Depends(get_db)):
    return db.query(ProductSpecification).all()


@router.get("/{specification_id}", response_model=ProductSpecificationRead)
def get_product_specification(specification_id: int, db: Session = Depends(get_db)):
    specification = db.query(ProductSpecification).filter(ProductSpecification.id == specification_id).first()
    if specification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product specification not found")
    return specification


@router.patch("/{specification_id}", response_model=ProductSpecificationRead)
def update_product_specification(
    specification_id: int, payload: ProductSpecificationUpdate, db: Session = Depends(get_db)
):
    specification = db.query(ProductSpecification).filter(ProductSpecification.id == specification_id).first()
    if specification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product specification not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(specification, field, value)

    db.commit()
    db.refresh(specification)
    return specification


@router.delete("/{specification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_specification(specification_id: int, db: Session = Depends(get_db)):
    specification = db.query(ProductSpecification).filter(ProductSpecification.id == specification_id).first()
    if specification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product specification not found")

    db.delete(specification)
    db.commit()