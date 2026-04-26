from fastapi import APIRouter
from app.api.endpoints import diagnosis, auth, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

# TODO: 추후 추가
# api_router.include_router(prescription.router, prefix="/prescription", tags=["prescription"])
# api_router.include_router(report.router, prefix="/report", tags=["report"])
