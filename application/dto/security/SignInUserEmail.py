from pydantic import BaseModel, EmailStr

class SignInUserEmail(BaseModel):

    email: EmailStr
    password: str
