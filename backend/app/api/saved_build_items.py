from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import SavedBuildItem
from app.schemas import SavedBuildItemCreate, SavedBuildItemUpdate, SavedBuildItemRead

router = APIRouter(prefix="/saved-build-items", tags=["Saved Build Items"])


@router.post("", response_model=SavedBuildItemRead, status_code=status.HTTP_201_CREATED)
def create_saved_build_item(payload: SavedBuildItemCreate, db: Session = Depends(get_db)):
    item = SavedBuildItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[SavedBuildItemRead])
def list_saved_build_items(db: Session = Depends(get_db)):
    return db.query(SavedBuildItem).all()


@router.get("/{item_id}", response_model=SavedBuildItemRead)
def get_saved_build_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(SavedBuildItem).filter(SavedBuildItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved build item not found")
    return item


@router.put("/{item_id}", response_model=SavedBuildItemRead)
def update_saved_build_item(item_id: int, payload: SavedBuildItemUpdate, db: Session = Depends(get_db)):
    item = db.query(SavedBuildItem).filter(SavedBuildItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved build item not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_build_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(SavedBuildItem).filter(SavedBuildItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved build item not found")

    db.delete(item)
    db.commit()