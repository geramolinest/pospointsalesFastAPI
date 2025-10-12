from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence import DbSession

class UnitOfWork:
    
    __db_context: AsyncSession
    
    def __init__(self, db_context: DbSession) -> None:
        self.__db_context = db_context
        
    async def save_changes_async(self) -> None:
        await self.__db_context.commit()