from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductReview
from app.schemas import ProductReviewCreate, ProductReviewUpdate, ProductReviewRead

router = APIRouter(prefix="/product-reviews", tags=["Product Reviews"])


@router.post("", response_model=ProductReviewRead, status_code=status.HTTP_201_CREATED)
def create_product_review(payload: ProductReviewCreate, db: Session = Depends(get_db)):
    review = ProductReview(**payload.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("", response_model=list[ProductReviewRead])
def list_product_reviews(db: Session = Depends(get_db)):
    return db.query(ProductReview).all()


@router.get("/{review_id}", response_model=ProductReviewRead)
def get_product_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ProductReview).filter(ProductReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product review not found")
    return review


@router.patch("/{review_id}", response_model=ProductReviewRead)
def update_product_review(review_id: int, payload: ProductReviewUpdate, db: Session = Depends(get_db)):
    review = db.query(ProductReview).filter(ProductReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product review not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ProductReview).filter(ProductReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product review not found")

    db.delete(review)
    db.commit()