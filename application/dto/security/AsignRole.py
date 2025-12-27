from pydantic import BaseModel

class AsignRole(BaseModel):
    role_name: str
    username: str   