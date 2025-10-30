import logging
from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import UsersRepository
from domain.entities import APIResponse, User
from utils.security import BCrypt, BCryptDep, JwtToken, JwtTokenDep

from .....dto.security import SignInUserUsername, Token, GetUser
from ....response.ServiceResponse import ServiceResponse


class SignInUsername:

    __repository: UsersRepository
    __bcrypt:  BCrypt
    __response: ServiceResponse[Token]
    __jwt: JwtToken

    def __init__(self, repository: Annotated[UsersRepository, Depends(UsersRepository)], bcrypt: BCryptDep, jwt: JwtTokenDep) -> None:
        self.__repository = repository
        self.__bcrypt = bcrypt
        self.__response = ServiceResponse[Token]()
        self.__jwt = jwt

    async def sign_in_user_by_username(self, sign_in_user: SignInUserUsername) -> APIResponse[Token]:
        try:

            user: User | None = await self.__repository.get_user_by_username( sign_in_user.username )

            if not user:
                return self.__response.unatuhorized_response(msg='Incorrect email or password') #type: ignore
            
            if not user.is_active:
                return self.__response.unatuhorized_response(msg='User is not active') #type: ignore
            
            if not self.__bcrypt.verify_password(sign_in_user.password, user.password):
                return self.__response.unatuhorized_response(msg='Incorrect email or password') #type: ignore
            
            userGet: GetUser = GetUser( **user.__dict__ )

            token: Token = self.__jwt.create_access_token( { **userGet.model_dump() } )

            return self.__response.ok_response(msg='User logged in successfully.', data=token)
        except Exception as e:
            logging.error(e)
            return self.__response.internal_server_error() #type: ignore