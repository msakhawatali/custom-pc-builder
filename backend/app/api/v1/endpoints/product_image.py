from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductImage
from app.schemas import ProductImageCreate, ProductImageUpdate, ProductImageRead

router = APIRouter(prefix="/product-images", tags=["Product Images"])


@router.post("", response_model=ProductImageRead, status_code=status.HTTP_201_CREATED)
def create_product_image(payload: ProductImageCreate, db: Session = Depends(get_db)):
    image = ProductImage(**payload.model_dump())
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.get("", response_model=list[ProductImageRead])
def list_product_images(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@router.get("/{image_id}", response_model=ProductImageRead)
def get_product_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")
    return image


@router.patch("/{image_id}", response_model=ProductImageRead)
def update_product_image(image_id: int, payload: ProductImageUpdate, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(image, field, value)

    db.commit()
    db.refresh(image)
    return image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")

    db.delete(image)
    db.commit()