from uuid import uuid4, UUID
from sqlalchemy import Uuid as ALQUUID, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[UUID]  = mapped_column(ALQUUID, primary_key=True, unique=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(25), unique=True,nullable=False)
    normalized_username: Mapped[str] = mapped_column(String(25), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    normalized_email: Mapped[str] = mapped_column(String(25), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles: Mapped[list['Role']] = relationship(secondary='roles_users', back_populates='users') # type: ignore

    
    