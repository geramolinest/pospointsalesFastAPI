from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities import Category
from infrastructure.persistence import DbSession

class CategoriesRepository:
    
    __db_context: AsyncSession
    
    def __init__(self, db_context: DbSession) -> None:
        self.__db_context = db_context
        
    async def get_all_categories(self) -> list[Category]:
        
        stmt = select(Category).where(Category.is_active).order_by(Category.id)
        
        result_promise = await self.__db_context.execute(stmt)
        
        scalars = result_promise.scalars().all()
        
        return [ *scalars]
    
    async def get_category_by_id(self, id: int) -> Category:
        
        stmt = select(Category).where(Category.id == id)
        
        promise = await self.__db_context.execute(stmt)
    
        return promise.scalar_one()
    
    async def add_category(self, category: Category) -> Category:
        
        self.__db_context.add( category )
        
        await self.__db_context.commit()
        
        await self.__db_context.refresh( category )
        
        return category
    
    async def get_category_by_name(self, category_name: str) -> Category:
        
        stmt = select(Category).where(Category.category_name == category_name.strip())
        
        promise = await self.__db_context.execute(stmt)
        
        return promise.scalar_one()
    
    async def any_category_by_name(self, category_name: str) -> bool:
        
        stmt = select(Category).where(Category.category_name == category_name.strip())
        
        promise = await self.__db_context.execute(stmt)
        
        result = promise.scalar_one_or_none()
        
        return result is not None