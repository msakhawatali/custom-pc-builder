from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductCompare
from app.schemas import ProductCompareCreate, ProductCompareUpdate, ProductCompareRead

router = APIRouter(prefix="/product-compares", tags=["Product Compares"])


@router.post("", response_model=ProductCompareRead, status_code=status.HTTP_201_CREATED)
def create_product_compare(user_id: int, payload: ProductCompareCreate, db: Session = Depends(get_db)):
    compare = ProductCompare(**payload.model_dump(), user_id=user_id)
    db.add(compare)
    db.commit()
    db.refresh(compare)
    return compare


@router.get("", response_model=list[ProductCompareRead])
def list_product_compares(db: Session = Depends(get_db)):
    return db.query(ProductCompare).all()


@router.get("/{compare_id}", response_model=ProductCompareRead)
def get_product_compare(compare_id: int, db: Session = Depends(get_db)):
    compare = db.query(ProductCompare).filter(ProductCompare.id == compare_id).first()
    if compare is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product compare not found")
    return compare


@router.put("/{compare_id}", response_model=ProductCompareRead)
def update_product_compare(compare_id: int, payload: ProductCompareUpdate, db: Session = Depends(get_db)):
    compare = db.query(ProductCompare).filter(ProductCompare.id == compare_id).first()
    if compare is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product compare not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(compare, field, value)

    db.commit()
    db.refresh(compare)
    return compare


@router.delete("/{compare_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_compare(compare_id: int, db: Session = Depends(get_db)):
    compare = db.query(ProductCompare).filter(ProductCompare.id == compare_id).first()
    if compare is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product compare not found")

    db.delete(compare)
    db.commit()