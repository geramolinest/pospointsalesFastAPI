from pydantic import BaseModel

class SignInUserUsername(BaseModel):
    username: str
    password: str