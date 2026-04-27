from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class STTResult:
    """STT 변환 결과 표준 모델"""
    transcript: str                  # 인식된 전체 텍스트
    confidence: float                # 전체 신뢰도 (0~1)
    words: list[dict] = field(default_factory=list)  # 단어별 타임스탬프/신뢰도
    duration_seconds: float = 0.0   # 음성 전체 길이
    error: Optional[str] = None     # 오류 메시지


class STTAdapter(ABC):
    """
    STT 벤더 추상 인터페이스.
    벤더 교체 시 이 클래스만 새로 구현하면 됩니다.
    (Clova → Google → OpenAI Whisper 등)
    """

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> STTResult:
        """
        음성 데이터를 텍스트로 변환합니다.
        
        Args:
            audio_bytes: PCM or WAV 형식의 음성 바이트
            sample_rate: 샘플레이트 (기본 16000Hz)
        
        Returns:
            STTResult: 변환 결과
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """STT 서비스 연결 상태를 확인합니다."""
        ...
