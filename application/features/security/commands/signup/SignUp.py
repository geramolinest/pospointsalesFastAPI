import logging
from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import UsersRepository
from domain.entities import APIResponse, User
from utils.security import BCryptDep, BCrypt, JwtToken, JwtTokenDep

from .....dto.security import SignUpUser, SignUpResponse, GetUser, Token
from ....response.ServiceResponse import ServiceResponse

class SignUp:
    
    __users_repository: UsersRepository
    __response: ServiceResponse[SignUpResponse]
    __bcrypt: BCrypt
    __jwt: JwtToken
    
    def __init__(self, repository: Annotated[UsersRepository, Depends(UsersRepository)], bcrypt: BCryptDep, jwt: JwtTokenDep) -> None:
        self.__users_repository = repository
        self.__response = ServiceResponse[SignUpResponse]()
        self.__bcrypt = bcrypt
        self.__jwt = jwt
        
    async def sign_up_user(self, signupUser: SignUpUser) -> APIResponse[SignUpResponse]:
        try:
            
            exists_user_name: User | None = await self.__users_repository.get_user_by_username( signupUser.username )
            
            if exists_user_name:
                return self.__response.bad_request_response(msg='Username already exists, please verify your username') #type: ignore
            
            exists_email: User | None = await self.__users_repository.get_user_by_email( signupUser.email )
            
            if exists_email:
                return self.__response.bad_request_response(msg='Email already exists, please verify your username') #type: ignore
            
            normalized_email: str = signupUser.email.upper()
            
            normalized_username: str = signupUser.username.upper()
            
            user_to_be_saved: User = User(**signupUser.model_dump())
            
            user_to_be_saved.normalized_email = normalized_email
            user_to_be_saved.normalized_username = normalized_username
            user_to_be_saved.password = self.__bcrypt.hash_password( signupUser.password )
            
            user_saved: User = await self.__users_repository.add_user( user_to_be_saved )
            
            user_to_be_returned: GetUser = GetUser( **user_saved.__dict__ )
            
            token: Token = self.__jwt.create_access_token( { **user_to_be_returned.model_dump() } )
            
            sign_up_response: SignUpResponse = SignUpResponse(user=user_to_be_returned, token=token)
            
            return self.__response.created_response(msg='User signed up successfully', data=sign_up_response)
        except Exception as e:            
            logging.error(e)
            return self.__response.internal_server_error() #type: ignore