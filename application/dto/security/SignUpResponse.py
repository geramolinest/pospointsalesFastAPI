from pydantic import BaseModel

from .GetUser import GetUser
from .Token import Token


class SignUpResponse(BaseModel):
    user: GetUser
    token: Token