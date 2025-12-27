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

                    is_authorized: bool = await users_repository.is_user_authorized( payload.username, [ role.upper().strip() for role in roles ] )
                    
                    if not is_authorized:
                        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={ **response_builder.forbidden_response().model_dump() })

            if iscoroutinefunction(handler):
                result: R = await handler(*args, **kwargs)
            else:
                sync_func = cast(Callable[...,R], handler)

                result: R = sync_func(*args, **kwargs)
            
            return result

        return wrapper
       
    return decorator