from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_role
from app.core.roles import UserRole
from app.models import User
from app.schemas import UserRead

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
