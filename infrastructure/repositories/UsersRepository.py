from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities import User
from infrastructure.persistence import DbSession

from utils import Config, ConfigDep
from utils.security import BCryptDep, BCrypt

class UsersRepository:
    
    __db_context: AsyncSession
    __config: Config
    __bcrypt: BCrypt
    
    def __init__(self, db_context: DbSession, config: ConfigDep, bcrypt: BCryptDep) -> None:
        self.__db_context = db_context
        self.__config = config
        self.__bcrypt = bcrypt
        
        
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
    
    