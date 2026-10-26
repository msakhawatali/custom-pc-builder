from fastapi import APIRouter, Depends

from app.api.dependencies import require_role
from app.core.roles import UserRole

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", dependencies=[Depends(require_role(UserRole.ADMIN))])
def admin_dashboard():
    return {"message": "Welcome to the admin dashboard"}