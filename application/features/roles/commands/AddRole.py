from logging import info

from fastapi import Depends
from typing import Annotated

from infrastructure.repositories import RolesRepository

from domain.entities import APIResponse, Role
from application.dto.security import AddRole, GetRole
from application.features.response.ServiceResponse import ServiceResponse

class AddRoleCommand:

    __roles_repository: RolesRepository
    __response: ServiceResponse[GetRole]

    def __init__(self, repository: Annotated[RolesRepository, Depends(RolesRepository)]) -> None:
        self.__roles_repository = repository
        self.__response = ServiceResponse[GetRole]()

    
    async def add_role(self, role: AddRole) -> APIResponse[GetRole]:

        try:
            role_exists = await self.__roles_repository.exists_role_async(role.role_name)
            
            if role_exists:
                return self.__response.bad_request_response( msg="Role already exists."   ) # type: ignore
            
            role_to_be_added = Role(
                role_name = role.role_name,
                normalized_role_name = role.role_name.strip().upper()
            )
            
            role_added: Role = await self.__roles_repository.add_role( role_to_be_added )

            return self.__response.ok_response(data=GetRole( **role_added.__dict__))
        
        except Exception as e:
            info("Exception occurred in AddRoleCommand.add_role: %s", str(e))
            return self.__response.internal_server_error() # type: ignore