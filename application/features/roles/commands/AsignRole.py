import logging
from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import UsersRepository, RolesRepository

from application.features.response.ServiceResponse import ServiceResponse
from domain.entities import APIResponse

class AsignRole:

    __users_repository: UsersRepository
    __response: ServiceResponse[str]
    __roles_respository: RolesRepository

    def __init__(self, users_repository: Annotated[UsersRepository, Depends(UsersRepository)], roles_respository: Annotated[RolesRepository, Depends(RolesRepository)]) -> None:
        self.__users_repository = users_repository
        self.__response = ServiceResponse[str]()
        self.__roles_respository = roles_respository

    
    async def asign_role_to_user(self, role_name: str, username: str) -> APIResponse[str]:

        try:
            user = await self.__users_repository.get_user_by_username( username )

            if not user:
                return self.__response.bad_request_response( msg="User does not exists." )  # type: ignore
            
            role = await self.__roles_respository.get_role_by_name( role_name )

            if not role:
                return self.__response.bad_request_response( msg="Role does not exists." )  # type: ignore

            has_role: bool = await self.__users_repository.is_user_authorized( user.username, [role.normalized_role_name])
            
            if has_role:
                return self.__response.bad_request_response( msg="User already has the role assigned." )  # type: ignore
            
            await self.__users_repository.asign_role_to_user( user, role )

            return self.__response.ok_response( data="Role assigned successfully." ) 
        
        except Exception as ex:
            logging.critical( f'Error assigning role to user: { ex }' )
            return self.__response.internal_server_error( )  # type: ignore