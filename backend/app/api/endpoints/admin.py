from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    role: Optional[UserRole] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(User.role != UserRole.admin)
    if role:
        query = query.where(User.role == role)
    query = query.offset(skip).limit(limit).order_by(User.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/users/count")
async def get_user_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User.role, func.count(User.id))
        .where(User.role != UserRole.admin)
        .group_by(User.role)
    )
    counts = {row[0].value: row[1] for row in result.all()}
    return {
        "student": counts.get("student", 0),
        "parent": counts.get("parent", 0),
        "teacher": counts.get("teacher", 0),
        "total": sum(counts.values()),
    }
