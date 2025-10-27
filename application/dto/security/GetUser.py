from pydantic import BaseModel, field_validator
from uuid import UUID
class GetUser(BaseModel):
    id: str
    username: str    
    email: str    
    is_active: bool
    
    @field_validator('id', mode='before')
    @classmethod
    def capitalize(cls, val: UUID) -> str:
        return str(val)
    