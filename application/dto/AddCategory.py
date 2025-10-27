from typing_extensions import Self
from pydantic import BaseModel, field_validator, model_validator, ValidationError

class AddCategory(BaseModel):
    
    category_name: str
    
    @field_validator('category_name', mode='before')
    @classmethod
    def capitalize(cls, val: str) -> str:
        return val.capitalize()
    
    @model_validator(mode='after')
    def check_category_length(self) -> Self:
        
        if self.category_name.__len__() > 50:
            raise ValidationError('Category name too long')
        
        return self