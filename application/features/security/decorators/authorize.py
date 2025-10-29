from fastapi import Request, status
from asyncio import iscoroutinefunction

from fastapi.exceptions import HTTPException

from functools import wraps
from typing import Any, Callable, Union, Awaitable, TypeVar, cast

from infrastructure.adapters.context import current_request
from application.features.response.ServiceResponse import ServiceResponse

from utils.security import JwtToken
from utils import Config

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

            if not request:
                print('Request is no present :(')
                raise Exception('Request is no present in http petition')
            
            config: Config = Config()

            jwt: JwtToken = JwtToken(config)

            response_builder = ServiceResponse[Any]()

            token_str: str | None = request.headers.get('authorization')

            if not token_str:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={ **response_builder.unatuhorized_response().model_dump() })
            
            token_str = token_str.replace('Bearer', '').strip()

            payload = jwt.verify_token( token_str )
            
            if not payload:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={ **response_builder.unatuhorized_response().model_dump() })
            
            print({ **payload.model_dump() })

            if iscoroutinefunction(handler):
                result: R = await handler(*args, **kwargs)
            else:
                sync_func = cast(Callable[...,R], handler)

                result: R = sync_func(*args, **kwargs)
            
            return result

        return wrapper
       
    return decorator