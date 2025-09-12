from venv import create
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(100))
    phone = Column(String(15), unique=True, index=True, nullable=True)
    dob = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)    