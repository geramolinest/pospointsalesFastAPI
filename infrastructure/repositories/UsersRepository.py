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
        
        await self.__db_context.commit()
        
        await self.__db_context.refresh(user)
        
        return user
    
    async def add_first_user(self) -> None:
        
        username = self.__config.get_value('ADMIN_USER')
        
        if not username:
            raise Exception('Username for admin user is not present')
        
        normalized_username: str = username.upper().strip()
        
        email_env: str | None = self.__config.get_value('ADMIN_USER_EMAIL')
        
        if not email_env:
            raise Exception('Email for admin user is not present')
        
        normalized_email: str = email_env.upper().strip()
        
        password: str | None = self.__config.get_value('ADMIN_USER_PASS')
        
        if not password:
            raise Exception('Password for admin user not present')
        
        password_hashed: str = self.__bcrypt.hash_password(password)
        
        user: User = User(
            username=username,
            normalized_username=normalized_username,
            email=email_env,
            normalized_email=normalized_email,
            password=password_hashed
        )
        
        self.__db_context.add(user)
        await self.__db_context.commit()