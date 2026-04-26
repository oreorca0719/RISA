from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.user import UserRole, GradeLevel


class UserRegister(BaseModel):
    username: str
    password: str
    name: str
    role: UserRole = UserRole.student
    grade: Optional[GradeLevel] = None

    @field_validator("username")
    @classmethod
    def username_min_length(cls, v: str) -> str:
        if len(v) < 4:
            raise ValueError("아이디는 4자 이상이어야 합니다.")
        return v

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("비밀번호는 6자 이상이어야 합니다.")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: UserRole
    grade: Optional[GradeLevel]
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
