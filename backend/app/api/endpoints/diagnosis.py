from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.core import (
    DiagnosisSession, FluencyResult, ComprehensionResult,
    SessionStatus, FluencyType
)
from app.schemas.diagnosis import (
    SessionCreate, SessionResponse,
    OralFluencySubmit, SilentFluencySubmit, FluencyResultResponse,
    ComprehensionSubmit, ComprehensionResultResponse,
    DiagnosisResultResponse
)

router = APIRouter()


@router.post("/session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(data: SessionCreate, student_id: int, db: AsyncSession = Depends(get_db)):
    """진단 세션 생성"""
    session = DiagnosisSession(
        student_id=student_id,
        text_id=data.text_id,
        status=SessionStatus.in_progress,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


@router.post("/fluency/oral", response_model=FluencyResultResponse, status_code=status.HTTP_201_CREATED)
async def submit_oral_fluency(data: OralFluencySubmit, db: AsyncSession = Depends(get_db)):
    """음독 유창성 결과 저장"""
    # 자동성: 10초당 정확 음절 수
    accurate_syllables = data.total_syllables - data.error_count
    automaticity = (accurate_syllables / data.reading_time_seconds) * 10 if data.reading_time_seconds > 0 else 0
    # 정확성: 1 - (오류수 / 총음절수)
    accuracy = 1 - (data.error_count / data.total_syllables) if data.total_syllables > 0 else 0

    result = FluencyResult(
        session_id=data.session_id,
        type=FluencyType.oral,
        reading_time_seconds=data.reading_time_seconds,
        total_syllables=data.total_syllables,
        error_count=data.error_count,
        automaticity_score=round(automaticity, 2),
        accuracy_score=round(accuracy, 4),
        raw_data=data.raw_data,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@router.post("/fluency/silent", response_model=FluencyResultResponse, status_code=status.HTTP_201_CREATED)
async def submit_silent_fluency(data: SilentFluencySubmit, db: AsyncSession = Depends(get_db)):
    """묵독 유창성 결과 저장"""
    result = FluencyResult(
        session_id=data.session_id,
        type=FluencyType.silent,
        silent_reading_time=data.silent_reading_time,
        comprehension_check_score=data.comprehension_check_score,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@router.post("/comprehension", response_model=ComprehensionResultResponse, status_code=status.HTTP_201_CREATED)
async def submit_comprehension(data: ComprehensionSubmit, db: AsyncSession = Depends(get_db)):
    """독해 문항 답변 저장 (채점은 추후 Claude API 연동)"""
    result = ComprehensionResult(
        session_id=data.session_id,
        question_type=data.question_type,
        question_index=data.question_index,
        answer=data.answer,
        # TODO: Claude API 채점 연동 (RIS-13)
        is_correct=None,
        score=None,
        ai_feedback=None,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@router.patch("/session/{session_id}/complete", response_model=SessionResponse)
async def complete_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """진단 세션 완료 처리"""
    from datetime import datetime, timezone
    result = await db.execute(select(DiagnosisSession).where(DiagnosisSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    session.status = SessionStatus.completed
    session.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(session)
    return session


@router.get("/result/{session_id}", response_model=DiagnosisResultResponse)
async def get_result(session_id: int, db: AsyncSession = Depends(get_db)):
    """진단 결과 조회"""
    result = await db.execute(select(DiagnosisSession).where(DiagnosisSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

    fluency_q = await db.execute(select(FluencyResult).where(FluencyResult.session_id == session_id))
    fluency_results = fluency_q.scalars().all()

    comp_q = await db.execute(select(ComprehensionResult).where(ComprehensionResult.session_id == session_id))
    comp_results = comp_q.scalars().all()

    # 유창성 점수 평균
    fluency_scores = [r.automaticity_score for r in fluency_results if r.automaticity_score is not None]
    total_fluency = round(sum(fluency_scores) / len(fluency_scores), 2) if fluency_scores else None

    # 독해 점수 평균
    comp_scores = [r.score for r in comp_results if r.score is not None]
    total_comp = round(sum(comp_scores) / len(comp_scores), 2) if comp_scores else None

    return DiagnosisResultResponse(
        session=session,
        fluency_results=fluency_results,
        comprehension_results=comp_results,
        total_fluency_score=total_fluency,
        total_comprehension_score=total_comp,
    )
