from pydantic import BaseModel, EmailStr

class SignInUser(BaseModel):

    email: EmailStr
    password: str
