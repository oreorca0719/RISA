import asyncio
from app.services.stt.adapter import STTAdapter, STTResult


class MockSTTAdapter(STTAdapter):
    """
    개발/테스트용 Mock STT 어댑터.
    Clova API 키 없이도 진단 플로우 전체를 테스트할 수 있습니다.
    """

    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> STTResult:
        # 실제 음성 길이 추정 (16bit PCM 기준)
        estimated_duration = len(audio_bytes) / (sample_rate * 2)
        await asyncio.sleep(0.1)  # API 호출 시뮬레이션

        return STTResult(
            transcript="[Mock] 오늘은 맑고 화창한 날씨입니다. 아이들이 운동장에서 뛰어놀고 있습니다.",
            confidence=0.95,
            words=[
                {"word": "오늘은", "start_ms": 0, "end_ms": 400, "confidence": 0.98},
                {"word": "맑고", "start_ms": 450, "end_ms": 700, "confidence": 0.96},
            ],
            duration_seconds=estimated_duration,
        )

    async def health_check(self) -> bool:
        return True
