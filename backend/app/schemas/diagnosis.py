from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.core import FluencyType, QuestionType, SessionStatus


class SessionCreate(BaseModel):
    text_id: Optional[int] = None


class SessionResponse(BaseModel):
    id: int
    student_id: int
    text_id: Optional[int]
    status: SessionStatus
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class OralFluencySubmit(BaseModel):
    session_id: int
    reading_time_seconds: float
    total_syllables: int
    error_count: int
    raw_data: Optional[dict] = None


class SilentFluencySubmit(BaseModel):
    session_id: int
    silent_reading_time: float
    comprehension_check_score: Optional[float] = None


class FluencyResultResponse(BaseModel):
    id: int
    session_id: int
    type: FluencyType
    automaticity_score: Optional[float]
    accuracy_score: Optional[float]
    silent_reading_time: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class ComprehensionSubmit(BaseModel):
    session_id: int
    question_type: QuestionType
    question_index: int
    answer: str


class ComprehensionResultResponse(BaseModel):
    id: int
    session_id: int
    question_type: QuestionType
    question_index: int
    is_correct: Optional[bool]
    score: Optional[float]
    ai_feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DiagnosisResultResponse(BaseModel):
    session: SessionResponse
    fluency_results: List[FluencyResultResponse]
    comprehension_results: List[ComprehensionResultResponse]
    total_fluency_score: Optional[float]
    total_comprehension_score: Optional[float]
