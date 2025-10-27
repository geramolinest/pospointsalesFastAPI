from typing import Annotated
from fastapi import Depends

from .BCrypt import BCrypt #type: ignore

from .JwtToken import JwtToken #type: ignore

BCryptDep = Annotated[BCrypt, Depends(BCrypt)]

JwtTokenDep = Annotated[JwtToken, Depends(JwtToken)]