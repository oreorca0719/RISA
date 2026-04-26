from pydantic import BaseModel, field_validator
from typing import Optional
from app.models.user import UserRole, Grade


class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str
    role: UserRole = UserRole.STUDENT
    grade: Optional[Grade] = None

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if len(v) < 4 or len(v) > 50:
            raise ValueError("아이디는 4~50자 사이여야 합니다.")
        return v

    @field_validator("password")
    @classmethod
    def password_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("비밀번호는 6자 이상이어야 합니다.")
        return v


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    role: str


class UserResponse(BaseModel):
    id: str
    username: str
    name: str
    role: str
    grade: Optional[str] = None
    is_active: bool

    model_config = {"from_attributes": True}
