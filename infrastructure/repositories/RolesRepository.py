from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.persistence import DbSession
from utils import ConfigDep
from domain.entities import Role

class RolesRepository:
    __db_context: AsyncSession
    
    def __init__(self, db_context: DbSession, config: ConfigDep) -> None:
        self.__db_context = db_context
        
    async def add_role(self, role: Role) -> Role:

        self.__db_context.add(role)
        
        await self.__db_context.flush()

        return role
    

    async def get_role_by_name(self, role_name: str) -> Role | None:
        
        stmt = select(Role).where(Role.normalized_role_name == role_name.strip().upper())

        result = await self.__db_context.execute( stmt )

        return result.scalar_one_or_none()
    
    async def get_role_by_id(self, id: str) -> Role | None:

        stmt = select(Role).where(Role.id == id.strip())

        result = await self.__db_context.execute( stmt )

        return result.scalar_one_or_none()
    
    async def get_all_roles(self, limit: int = 100, offset: int = 0) -> list[Role]:

        stmt = select(Role).limit(limit).offset(offset).order_by(Role.role_name.asc())

        result = await self.__db_context.execute( stmt )

        return [ *result.scalars().all() ]
    
    async def exists_role_async(self, role_name: str) -> bool:
        
        stmt = select(Role).where(Role.normalized_role_name == role_name.strip().upper())
        
        result = await self.__db_context.execute( stmt )

        return not result.scalar_one_or_none() is None
    