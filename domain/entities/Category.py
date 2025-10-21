from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base

class Category(Base):
    
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    