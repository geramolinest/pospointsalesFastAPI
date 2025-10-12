from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    status_code: int
    status_text: str
    data: T
    message: str
    