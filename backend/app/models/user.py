from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.models.base import Base
from app.core.roles import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(20), default=UserRole.USER.value, server_default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)