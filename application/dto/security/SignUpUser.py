from pydantic import BaseModel, EmailStr, Field

class SignUpUser(BaseModel):
        
    username: str = Field(max_length=25, min_length=8)   
    email: EmailStr    
    password: str = Field(max_length=25, min_length=8)