from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import Wishlist
from app.schemas import WishlistCreate, WishlistUpdate, WishlistRead

router = APIRouter(prefix="/wishlists", tags=["Wishlists"])


@router.post("", response_model=WishlistRead, status_code=status.HTTP_201_CREATED)
def create_wishlist(payload: WishlistCreate, db: Session = Depends(get_db)):
    wishlist = Wishlist(**payload.model_dump())
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)
    return wishlist


@router.get("", response_model=list[WishlistRead])
def list_wishlists(db: Session = Depends(get_db)):
    return db.query(Wishlist).all()


@router.get("/{wishlist_id}", response_model=WishlistRead)
def get_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found")
    return wishlist


@router.patch("/{wishlist_id}", response_model=WishlistRead)
def update_wishlist(wishlist_id: int, payload: WishlistUpdate, db: Session = Depends(get_db)):
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(wishlist, field, value)

    db.commit()
    db.refresh(wishlist)
    return wishlist


@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found")

    db.delete(wishlist)
    db.commit()