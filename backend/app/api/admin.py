from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_role
from app.db.dependencies import get_db
from app.core.roles import UserRole
from app.models import User
from app.schemas import UserRead, UserStatusUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", dependencies=[Depends(require_role(UserRole.ADMIN))])
def admin_dashboard():
    return {"message": "Welcome to the admin dashboard"}


@router.get(
    "/users",
    response_model=list[UserRead],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def admin_list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()

@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def admin_get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch(
    "/users/{user_id}/status",
    response_model=UserRead,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def admin_update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user
