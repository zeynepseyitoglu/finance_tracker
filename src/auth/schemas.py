from pydantic import BaseModel, EmailStr


class Userbase(BaseModel):
    email: EmailStr

class UserCreate(Userbase):
    password: str

class UserResponse(Userbase):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}

class LoginRequest(Userbase):
    password: str