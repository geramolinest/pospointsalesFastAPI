from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.persistence import DbSession
from utils import ConfigDep, Config
from domain.entities import Role, User

class RolesRepository:
    __db_context: AsyncSession
    __config: Config
    
    def __init__(self, db_context: DbSession, config: ConfigDep) -> None:
        self.__db_context = db_context
        self.__config = config

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

        stmt = select(Role).limit(limit).offset(offset).order_by(Role.id.asc())

        result = await self.__db_context.execute( stmt )

        return [ *result.scalars().all() ]
    
    async def exists_role_async(self, role_name: str) -> bool:
        
        stmt = select(Role).where(Role.normalized_role_name == role_name.strip().upper())
        
        result = await self.__db_context.execute( stmt )

        return not result.scalar_one_or_none() is None
    
    async def add_admin_role_and_asign(self) -> None:

        admin_role_name: str = self.__config.get_value('ADMIN_ROLE') or 'ADMIN'

        #Verify if role exists
        exists_admin_role: bool = await self.exists_role_async( admin_role_name )

        if exists_admin_role:
            return
        
        role: Role = Role(role_name = admin_role_name.strip(), normalized_role_name = admin_role_name.upper().strip())

        admin_user_env:str = self.__config.get_value('ADMIN_USER') or ''

        stmt_admin_user = select(User).where(User.normalized_username == admin_user_env.upper().strip())

        promise_admin_user = await self.__db_context.execute( stmt_admin_user )

        admin_user = promise_admin_user.scalar_one_or_none()

        if not admin_user:
            raise Exception('Admin user is not present, please validate')
        
        admin_user.roles.append( role ) #type: ignore
        
        await self.__db_context.flush()
