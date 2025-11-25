import logging
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
    
    async def user_me_by_username(self, user_name: str) -> User | None:
        
        stmt = select(User).where(User.normalized_username == user_name.upper().strip())
        
        result = await self.__db_context.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def add_admin_user(self) -> None:
        
        username = self.__config.get_value('ADMIN_USER')
        
        if not username:
            raise Exception('Username for admin user is not present')
        
        normalized_username: str = username.upper().strip()
        
        email_env: str | None = self.__config.get_value('ADMIN_USER_EMAIL')
        
        if not email_env:
            raise Exception('Email for admin user is not present')
        
        normalized_email: str = email_env.upper().strip()

        #Verify if username provided for admin user already exists in DB
        exists_username: User | None = await self.get_user_by_username( username )
        
        #Verify if email provided for admin user already exists in DB
        exists_email = await self.get_user_by_email( email_env )

        if exists_username or exists_email:
            logging.warning('Email or username provided for admin user in environment already exists, verify if you have an admin user')
            return
        
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
        await self.__db_context.flush()