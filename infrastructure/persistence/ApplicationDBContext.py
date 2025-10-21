import logging

import os
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

from domain.entities import Base, Category, Role, User, RoleUser # type: ignore

class ApplicationDBContext:
    
    __engine: AsyncEngine
    __session: async_sessionmaker[AsyncSession]
    
    def __new__(cls):
        
        if not hasattr(cls, '_instance'):
            logging.info('Setting DBContext')
            cls._instance = super(ApplicationDBContext, cls).__new__(cls)          
            logging.info('Setting DBContext done')
            cls._instance.__build_engine()
            #loop = asyncio.get_event_loop()
            #loop.create_task(cls._instance.__sync_database())
            cls._instance.__build_session()
            
        return cls._instance
    
    def __build_engine(self) -> None:
        
        uri_env  = os.getenv('DATABASE_URI')
        
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