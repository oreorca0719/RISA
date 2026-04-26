from fastapi import APIRouter
from app.api.endpoints import diagnosis, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])

# TODO: 추후 추가
# api_router.include_router(prescription.router, prefix="/prescription", tags=["prescription"])
# api_router.include_router(report.router, prefix="/report", tags=["report"])
