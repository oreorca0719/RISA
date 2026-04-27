import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TextGrade(str, enum.Enum):
    elem4 = "elem4"
    elem5 = "elem5"
    elem6 = "elem6"


class TextGenre(str, enum.Enum):
    narrative = "narrative"    # 이야기글
    expository = "expository"  # 설명글


class TextLevel(str, enum.Enum):
    low = "low"
    mid = "mid"
    high = "high"


class TextStatus(str, enum.Enum):
    draft = "draft"
    reviewing = "reviewing"
    approved = "approved"


class TextSource(str, enum.Enum):
    ai_generated = "ai_generated"
    manual = "manual"


class SessionStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class FluencyType(str, enum.Enum):
    oral = "oral"
    silent = "silent"


class QuestionType(str, enum.Enum):
    factual = "factual"        # 사실적 이해
    inferential = "inferential" # 추론적 이해
    critical = "critical"      # 비판적 이해


class ReaderType(str, enum.Enum):
    avid = "avid"              # 애독자
    intermittent = "intermittent"  # 간헐적 독자
    non_reader = "non_reader"  # 비독자


class ReadingLevel(str, enum.Enum):
    low = "low"
    mid = "mid"
    high = "high"


class ReportRole(str, enum.Enum):
    student = "student"
    parent = "parent"
    teacher = "teacher"


class UserRelation(Base):
    __tablename__ = "user_relations"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('parent_id', 'student_id', name='uq_user_relations'),)


class TextContent(Base):
    __tablename__ = "texts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    grade = Column(Enum(TextGrade), nullable=False)
    genre = Column(Enum(TextGenre), nullable=False)
    level = Column(Enum(TextLevel), nullable=False)
    word_count = Column(Integer, nullable=True)
    status = Column(Enum(TextStatus), nullable=False, default=TextStatus.draft)
    source = Column(Enum(TextSource), nullable=False, default=TextSource.ai_generated)
    metadata_ = Column("metadata", JSONB, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DiagnosisSession(Base):
    __tablename__ = "diagnosis_sessions"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    text_id = Column(Integer, ForeignKey('texts.id', ondelete='SET NULL'), nullable=True)
    status = Column(Enum(SessionStatus), nullable=False, default=SessionStatus.in_progress)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    fluency_results = relationship("FluencyResult", back_populates="session")
    comprehension_results = relationship("ComprehensionResult", back_populates="session")


class FluencyResult(Base):
    __tablename__ = "fluency_results"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('diagnosis_sessions.id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum(FluencyType), nullable=False)
    reading_time_seconds = Column(Float, nullable=True)
    total_syllables = Column(Integer, nullable=True)
    error_count = Column(Integer, nullable=True)
    automaticity_score = Column(Float, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    silent_reading_time = Column(Float, nullable=True)
    comprehension_check_score = Column(Float, nullable=True)
    raw_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("DiagnosisSession", back_populates="fluency_results")


class ComprehensionResult(Base):
    __tablename__ = "comprehension_results"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('diagnosis_sessions.id', ondelete='CASCADE'), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    question_index = Column(Integer, nullable=False)
    answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    score = Column(Float, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("DiagnosisSession", back_populates="comprehension_results")


class ReaderProfile(Base):
    __tablename__ = "reader_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_id = Column(Integer, ForeignKey('diagnosis_sessions.id', ondelete='SET NULL'), nullable=True)
    reader_type = Column(Enum(ReaderType), nullable=False)
    reading_level = Column(Enum(ReadingLevel), nullable=False)
    fluency_score = Column(Float, nullable=True)
    comprehension_score = Column(Float, nullable=True)
    total_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_id = Column(Integer, ForeignKey('diagnosis_sessions.id', ondelete='SET NULL'), nullable=True)
    profile_id = Column(Integer, ForeignKey('reader_profiles.id', ondelete='SET NULL'), nullable=True)
    prescription_matrix = Column(String(10), nullable=True)
    recommended_texts = Column(JSONB, nullable=True)
    ai_recommendation = Column(Text, nullable=True)
    reading_goal = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_id = Column(Integer, ForeignKey('diagnosis_sessions.id', ondelete='SET NULL'), nullable=True)
    target_role = Column(Enum(ReportRole), nullable=False)
    content = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
