from pydantic import BaseModel

class GetCategory(BaseModel):
    id: int
    category_name: str
    is_active: bool