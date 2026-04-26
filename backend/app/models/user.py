import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class UserRole(str, PyEnum):
    STUDENT = "student"
    PARENT  = "parent"
    TEACHER = "teacher"
    ADMIN   = "admin"


class Grade(str, PyEnum):
    ELEM1 = "elem1"
    ELEM2 = "elem2"
    ELEM3 = "elem3"
    ELEM4 = "elem4"
    ELEM5 = "elem5"
    ELEM6 = "elem6"
    MID1  = "mid1"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    grade: Mapped[str | None] = mapped_column(Enum(Grade), nullable=True)  # 학생만
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계 (부모-자녀, 교사-학생)
    children: Mapped[list["UserRelation"]] = relationship(
        "UserRelation", foreign_keys="UserRelation.parent_id", back_populates="parent"
    )
    parents: Mapped[list["UserRelation"]] = relationship(
        "UserRelation", foreign_keys="UserRelation.child_id", back_populates="child"
    )


class UserRelation(Base):
    """부모-자녀 / 교사-학생 연결 테이블"""
    __tablename__ = "user_relations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    relation_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "parent" | "teacher"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    parent: Mapped["User"] = relationship("User", foreign_keys=[parent_id], back_populates="children")
    child: Mapped["User"] = relationship("User", foreign_keys=[child_id], back_populates="parents")
