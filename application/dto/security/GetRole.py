from pydantic import field_validator, BaseModel
from uuid import UUID

class GetRole(BaseModel):
    id: str
    role_name: str
    normalized_role_name: str

    @field_validator('id', mode='before')
    @classmethod
    def capitalize(cls, val: UUID) -> str:
        return str(val)