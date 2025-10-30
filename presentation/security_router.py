from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException

from domain.entities import APIResponse
from application.dto.security import SignInUserEmail, SignUpResponse, SignUpUser, Token, SignInUserUsername
from application.features.security.commands import SignUp, SignInEmail, SignInUsername

security_router: APIRouter = APIRouter(prefix='/users', tags=['Security'])

@security_router.post('/sign-up', status_code=201)
async def sign_up_user(sign_up_user: SignUpUser, service: Annotated[SignUp, Depends(SignUp)]) -> APIResponse[SignUpResponse]:
    
    result: APIResponse[SignUpResponse] = await service.sign_up_user( sign_up_user )
    
    if result.status_code > 299:
        raise HTTPException(result.status_code, detail={ **result.model_dump() })
    
    
    return result

@security_router.post('/sign-in-email', status_code=200)
async def sign_in_user_by_email(sign_in_user: SignInUserEmail, service: Annotated[SignInEmail,Depends(SignInEmail)]) ->APIResponse[Token]:
    
    result: APIResponse[Token] = await service.sign_in_user_by_email( sign_in_user )

    if result.status_code > 299:
        raise HTTPException(result.status_code, detail={ **result.model_dump() })
    
    return result

@security_router.post('/sign-in-username', status_code=200)
async def sign_in_user_by_username(sign_in_user: SignInUserUsername, service: Annotated[SignInUsername,Depends(SignInUsername)]) ->APIResponse[Token]:
    
    result: APIResponse[Token] = await service.sign_in_user_by_username( sign_in_user )

    if result.status_code > 299:
        raise HTTPException(result.status_code, detail={ **result.model_dump() })
    
    return result