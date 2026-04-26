from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.user_service import get_user_by_username, create_user, authenticate_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_username(db, data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 아이디입니다."
        )
    user = await create_user(db, data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
async def get_me():
    # TODO: JWT 미들웨어에서 현재 사용자 추출
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="준비 중")
