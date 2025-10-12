from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from .ApplicationDBContext import ApplicationDBContext

async def get_session_dependency():
    
    db_context: ApplicationDBContext = ApplicationDBContext()
    
    async with db_context.get_session()() as session:
        yield session
        
        
DbSession = Annotated[AsyncSession, Depends(get_session_dependency)]