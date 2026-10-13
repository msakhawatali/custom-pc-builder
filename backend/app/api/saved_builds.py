from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import SavedBuild
from app.schemas import SavedBuildCreate, SavedBuildUpdate, SavedBuildRead

router = APIRouter(prefix="/saved-builds", tags=["Saved Builds"])


@router.post("", response_model=SavedBuildRead, status_code=status.HTTP_201_CREATED)
def create_saved_build(user_id: int, payload: SavedBuildCreate, db: Session = Depends(get_db)):
    saved_build = SavedBuild(**payload.model_dump(), user_id=user_id)
    db.add(saved_build)
    db.commit()
    db.refresh(saved_build)
    return saved_build


@router.get("", response_model=list[SavedBuildRead])
def list_saved_builds(db: Session = Depends(get_db)):
    return db.query(SavedBuild).all()


@router.get("/{saved_build_id}", response_model=SavedBuildRead)
def get_saved_build(saved_build_id: int, db: Session = Depends(get_db)):
    saved_build = db.query(SavedBuild).filter(SavedBuild.id == saved_build_id).first()
    if saved_build is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved build not found")
    return saved_build


@router.put("/{saved_build_id}", response_model=SavedBuildRead)
def update_saved_build(saved_build_id: int, payload: SavedBuildUpdate, db: Session = Depends(get_db)):
    saved_build = db.query(SavedBuild).filter(SavedBuild.id == saved_build_id).first()
    if saved_build is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved build not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(saved_build, field, value)

    db.commit()
    db.refresh(saved_build)
    return saved_build


@router.delete("/{saved_build_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_build(saved_build_id: int, db: Session = Depends(get_db)):
    saved_build = db.query(SavedBuild).filter(SavedBuild.id == saved_build_id).first()
    if saved_build is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved build not found")

    db.delete(saved_build)
    db.commit()