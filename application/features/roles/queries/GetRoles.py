from logging import info
from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import RolesRepository

from application.dto.security import GetRole
from application.features.response.ServiceResponse import ServiceResponse

from domain.entities import APIResponse

class GetRolesQuery:

    __repository: RolesRepository
    __response: ServiceResponse[list[GetRole]]

    def __init__(self, repository: Annotated[RolesRepository, Depends(RolesRepository)]) -> None:
        self.__repository = repository
        self.__response = ServiceResponse[list[GetRole]]()

    async def get_roles(self, limit: int = 100, offset: int = 0) -> APIResponse[list[GetRole]]:
        try:
            
            roles = await self.__repository.get_all_roles(limit, offset)

            role_dtos: list[GetRole] = [ GetRole(**role.__dict__) for role in roles ] 

            return self.__response.ok_response(data=role_dtos)
        
        except Exception as e:
            info("Error trying to get roles from db  ", str(e))
            return self.__response.internal_server_error()  # type: ignore 