import logging
from fastapi import Request, status
from asyncio import iscoroutinefunction

from fastapi.exceptions import HTTPException

from functools import wraps
from typing import Any, Callable, Union, Awaitable, TypeVar, cast

from infrastructure.adapters.context import current_request
from application.features.response.ServiceResponse import ServiceResponse
from application.dto.security import GetUser

from utils.security import JwtToken
from utils import Config
from infrastructure.repositories import UsersRepository
from infrastructure.persistence import ApplicationDBContext


R = TypeVar('R')

RouteHandler = Union[
    Callable[..., Awaitable[R]],  # async def
    Callable[..., R],             # sync def
]

def authorize( roles: list[str] = [] ) -> Callable[[RouteHandler[R]], RouteHandler[R]]:

    def decorator(handler: RouteHandler[R]) -> RouteHandler[R]:
        @wraps(handler)
        async def wrapper(*args: Any,**kwargs: Any) -> Any:
            
            request: Request | None = current_request.get()

            response_builder = ServiceResponse[Any]()

            if not request:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail={ **response_builder.internal_server_error().model_dump() })
            
            config: Config = Config()

            jwt: JwtToken = JwtToken(config)

            token_str: str | None = request.headers.get('authorization')

            if not token_str:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={ **response_builder.unatuhorized_response().model_dump() })
            
            token_str = token_str.replace('Bearer', '').strip()

            payload: GetUser | None = jwt.verify_token( token_str )
            
            if not payload:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={ **response_builder.unatuhorized_response().model_dump() })
            
            logging.info({ **payload.model_dump() })

            if roles.__len__():
                logging.info('Roles required for this endpoint')

                async with ApplicationDBContext().get_session()() as session:

                    users_repository: UsersRepository = UsersRepository( session )

                    roles_from_db: list[str] | None = await users_repository.get_roles_by_username( payload.username)

                    if not roles_from_db:
                        logging.info('No roles found for this user, raising forbidden exception')
                        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={ **response_builder.forbidden_response().model_dump() })

                    authorized_flag: bool = False
                    
                    logging.info('Roles from DB founded for this user')

                    for role in roles:
                        if role.upper().strip() in roles_from_db:
                            logging.info(f'Role {role} authorized')
                            authorized_flag = True
                            break
                    
                    if not authorized_flag:
                        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={ **response_builder.forbidden_response().model_dump() })

            if iscoroutinefunction(handler):
                result: R = await handler(*args, **kwargs)
            else:
                sync_func = cast(Callable[...,R], handler)

                result: R = sync_func(*args, **kwargs)
            
            return result

        return wrapper
       
    return decorator