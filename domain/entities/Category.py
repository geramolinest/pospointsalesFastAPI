
from sqlalchemy import Column, Integer, String, Boolean

from .Base import Base

class Category(Base):
    
    __tablename__ = 'categories'
    
    id: Column[int] = Column(Integer, primary_key=True)
    category_name: Column[str] = Column(String(50), unique=True)
    is_active: Column[bool] = Column(Boolean, default=True)
    