from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

from .Base import Base

class RoleUser(Base):
    
    __tablename__ = 'roles_users'
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)