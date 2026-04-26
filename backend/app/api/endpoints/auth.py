from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login():
    # TODO: JWT 인증 구현
    return {"message": "not implemented"}


@router.post("/register")
async def register():
    # TODO: 회원가입 구현
    return {"message": "not implemented"}


@router.post("/refresh")
async def refresh_token():
    # TODO: 토큰 갱신 구현
    return {"message": "not implemented"}
