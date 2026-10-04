from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import WishlistItem
from app.schemas import WishlistItemCreate, WishlistItemUpdate, WishlistItemRead

router = APIRouter(prefix="/wishlist-items", tags=["Wishlist Items"])


@router.post("", response_model=WishlistItemRead, status_code=status.HTTP_201_CREATED)
def create_wishlist_item(payload: WishlistItemCreate, db: Session = Depends(get_db)):
    item = WishlistItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[WishlistItemRead])
def list_wishlist_items(db: Session = Depends(get_db)):
    return db.query(WishlistItem).all()


@router.get("/{wishlist_item_id}", response_model=WishlistItemRead)
def get_wishlist_item(wishlist_item_id: int, db: Session = Depends(get_db)):
    item = db.query(WishlistItem).filter(WishlistItem.id == wishlist_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")
    return item


@router.patch("/{wishlist_item_id}", response_model=WishlistItemRead)
def update_wishlist_item(wishlist_item_id: int, payload: WishlistItemUpdate, db: Session = Depends(get_db)):
    item = db.query(WishlistItem).filter(WishlistItem.id == wishlist_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{wishlist_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist_item(wishlist_item_id: int, db: Session = Depends(get_db)):
    item = db.query(WishlistItem).filter(WishlistItem.id == wishlist_item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")

    db.delete(item)
    db.commit()