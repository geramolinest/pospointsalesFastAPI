import logging

from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import UsersRepository
from domain.entities import APIResponse, User

from ....response.ServiceResponse import ServiceResponse
from .....dto.security import GetUser


class UserMeFeature:
    
    __respository: UsersRepository
    __response: ServiceResponse[GetUser]

    def __init__(self, repository: Annotated[UsersRepository, Depends(UsersRepository)]) -> None:
        self.__respository = repository
        self.__response = ServiceResponse[GetUser]()

    
    async def user_me_username(self, username: str) -> APIResponse[GetUser]:

        try:
            response: User | None = await self.__respository.get_user_by_username( username )

            if response is None:
                return self.__response.not_found_response(msg='User does not exists') #type: ignore

            return self.__response.ok_response(msg='User fetched successfully', data=GetUser(**response.__dict__))
        except Exception as e:
            logging.error(e)
            return self.__response.internal_server_error()  # type: ignore

        