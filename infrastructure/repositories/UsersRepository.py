from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities import User
from infrastructure.persistence import DbSession

class UsersRepository:
    
    __db_context: AsyncSession
    
    def __init__(self, db_context: DbSession) -> None:
        self.__db_context = db_context    
        
    async def get_user_by_email(self, email: str) -> User | None:
        
        stmt = select(User).where(User.normalized_email == email.upper().strip())
        
        result = await self.__db_context.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> User | None:
        
        stmt = select(User).where(User.normalized_username == username.upper().strip())
        
        result = await self.__db_context.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, id: str) -> User | None:
        
        stmt = select(User).where(User.id == id.strip())
        
        result =  await self.__db_context.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def add_user(self, user: User) -> User:
        
        self.__db_context.add(user)
        
        await self.__db_context.flush()
    
        return user

    async def get_roles_by_username(self, username: str) -> list[str] | None:
        
        stmt = select(User).options(selectinload(User.roles)).where(User.normalized_username == username.upper().strip() ) #type: ignore

        result = await self.__db_context.execute( stmt )

        user: User | None = result.scalar_one_or_none()

        if not user:
            return None
        
        user_roles: list[str] = [ role.normalized_role_name for role in user.roles ] #type: ignore
        
        return user_roles