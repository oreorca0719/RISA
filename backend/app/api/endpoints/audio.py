from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.stt import MockSTTAdapter, ClovaSTTAdapter
from app.services.stt.analyzer import analyze_oral_reading
from app.core.config import settings

router = APIRouter()


def get_stt_adapter():
    """환경에 따라 STT 어댑터를 선택합니다."""
    if settings.CLOVA_API_KEY:
        return ClovaSTTAdapter()
    return MockSTTAdapter()


@router.post("/oral")
async def transcribe_oral_reading(
    audio: UploadFile = File(..., description="음성 파일 (WAV, PCM)"),
    original_text: str = Form(..., description="원본 지문 텍스트"),
    reading_time_seconds: float = Form(..., description="실제 낭독 소요 시간(초)"),
):
    """
    음독 음성 파일을 STT로 변환하고 유창성 점수를 계산합니다.
    결과를 diagnosis/fluency/oral 엔드포인트로 저장하는 데 사용하세요.
    """
    if not audio.content_type.startswith(("audio/", "application/octet-stream")):
        raise HTTPException(status_code=400, detail="오디오 파일만 업로드 가능합니다.")

    audio_bytes = await audio.read()
    if len(audio_bytes) > 10 * 1024 * 1024:  # 10MB 제한
        raise HTTPException(status_code=400, detail="파일 크기는 10MB 이하여야 합니다.")

    adapter = get_stt_adapter()
    stt_result = await adapter.transcribe(audio_bytes)

    if stt_result.error:
        raise HTTPException(status_code=502, detail=f"STT 오류: {stt_result.error}")

    analysis = analyze_oral_reading(
        original_text=original_text,
        transcript=stt_result.transcript,
        reading_time_seconds=reading_time_seconds,
    )

    return {
        "transcript": stt_result.transcript,
        "confidence": stt_result.confidence,
        "duration_seconds": stt_result.duration_seconds,
        "analysis": {
            "automaticity_score": analysis.automaticity_score,
            "accuracy_score": analysis.accuracy_score,
            "error_count": analysis.error_count,
            "total_syllables": analysis.total_syllables,
            "accurate_syllables": analysis.accurate_syllables,
        },
        "stt_adapter": "clova" if settings.CLOVA_API_KEY else "mock",
    }


@router.get("/health")
async def stt_health():
    """STT 서비스 연결 상태를 확인합니다."""
    adapter = get_stt_adapter()
    is_healthy = await adapter.health_check()
    return {
        "status": "ok" if is_healthy else "unavailable",
        "adapter": "clova" if settings.CLOVA_API_KEY else "mock",
    }
