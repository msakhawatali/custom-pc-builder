from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.text import slugify
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductCategory
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate, ProductCategoryRead

router = APIRouter(prefix="/categories", tags=["Product Categories"])


@router.post("", response_model=ProductCategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: ProductCategoryCreate, db: Session = Depends(get_db)):
    category = ProductCategory(**payload.model_dump(), slug=slugify(payload.name),)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("", response_model=list[ProductCategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(ProductCategory).all()


@router.get("/{category_id}", response_model=ProductCategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=ProductCategoryRead)
def update_category(category_id: int, payload: ProductCategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    if "name" in update_data:
        category.slug = slugify(update_data["name"])

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()