import logging
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .ApplicationDBContext import ApplicationDBContext

async def get_session_dependency():
    
    db_context: ApplicationDBContext = ApplicationDBContext()
    
    async with db_context.get_session()() as session:
        try:
            logging.debug('Databse connection traced')
            logging.debug({ **session.info })
            yield session
            logging.info('Commiting changes')
            await session.commit()
        except SQLAlchemyError as e:
            logging.error('An error ocurred, applying rollback to database changes', e)
            await session.rollback()
            raise
        except Exception as e:
            raise
        finally:
            await session.close()
        
        
DbSession = Annotated[AsyncSession, Depends(get_session_dependency)]