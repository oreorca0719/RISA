import httpx
import uuid
from app.services.stt.adapter import STTAdapter, STTResult
from app.core.config import settings


class ClovaSTTAdapter(STTAdapter):
    """
    Naver Clova Speech Recognition (CSR) 어댑터.
    RIS-11 파일럿 테스트 완료 후 실제 API 키로 활성화.
    """

    BASE_URL = "https://clovaspeech-gw.ncloud.com/recog/v1/stt"

    def __init__(self):
        self.api_key = settings.CLOVA_API_KEY
        self.headers = {
            "X-CLOVASPEECH-API-ID": self.api_key,
            "Content-Type": "application/octet-stream",
        }

    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> STTResult:
        if not self.api_key:
            return STTResult(
                transcript="",
                confidence=0.0,
                error="CLOVA_API_KEY가 설정되지 않았습니다. MockSTTAdapter를 사용하세요."
            )

        params = {
            "lang": "Kor",
            "assessment": "false",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.BASE_URL,
                    headers=self.headers,
                    params=params,
                    content=audio_bytes,
                )
                response.raise_for_status()
                data = response.json()

                return STTResult(
                    transcript=data.get("text", ""),
                    confidence=data.get("confidence", 0.0),
                    words=data.get("words", []),
                    duration_seconds=data.get("duration", 0.0) / 1000,
                )
        except httpx.HTTPStatusError as e:
            return STTResult(transcript="", confidence=0.0, error=f"Clova API 오류: {e.response.status_code}")
        except Exception as e:
            return STTResult(transcript="", confidence=0.0, error=str(e))

    async def health_check(self) -> bool:
        return bool(self.api_key)
