import logging

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy import select

from utils import Config

from domain.entities import Base, Category, Role, User, RoleUser # type: ignore

class ApplicationDBContext:
    
    __engine: AsyncEngine
    __session: async_sessionmaker[AsyncSession]
    __config: Config
    
    def __new__(cls):
        
        if not hasattr(cls, '_instance'):
            logging.info('Setting DBContext')
            cls._instance = super(ApplicationDBContext, cls).__new__(cls)
            cls._instance.__config = Config()          
            
            logging.info('Setting DBContext done')
            cls._instance.__build_engine()
            #loop = asyncio.get_event_loop()
            #loop.create_task(cls._instance.__sync_database())
            cls._instance.__build_session()

            # Seed database
            loop = asyncio.get_event_loop()
            loop.create_task(cls._instance.__seed_database())
            
        return cls._instance
    
    def __build_engine(self) -> None:
        
        uri_env  = self.__config.get_value('DATABASE_URI')
        
        if not uri_env:
            raise Exception('DATABASE URI not provided')
        
        logging.info(uri_env)
        
        self.__engine = create_async_engine(uri_env, echo=True)
        
    async def sync_database(self) -> None:
    
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await asyncio.sleep(0)       
        
    def get_engine(self) -> AsyncEngine:
        return self.__engine
    
    def __build_session(self) -> None:
        self.__session = async_sessionmaker(bind=self.get_engine())
    
    def get_session(self) -> async_sessionmaker[AsyncSession]:
        return self.__session
    
    async def __seed_database(self) -> None:
        
        async with self.get_session()() as session:
            
            user: User = User.get_admin_user( self.__config )

            stmt = select(User).where(User.normalized_username == user.normalized_username )

            result = await session.execute( stmt )

            if result.scalar_one_or_none() is not None:
                logging.info('Admin user already exists')
                return
            
            role: Role = Role.get_admin_role( self.__config )

            stmt_role = select(Role).where(Role.normalized_role_name == role.normalized_role_name )

            result_role = await session.execute( stmt_role )

            if result_role.scalar_one_or_none() is not None:
                logging.info('Admin role already exists')
            
            user.roles.append( role ) # type: ignore

            session.add( user )

            await session.commit()



