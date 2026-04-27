"""
음독 오류 분석기.
STT 결과와 원본 텍스트를 비교해 자동성/정확성 점수를 계산합니다.
"""
from dataclasses import dataclass


@dataclass
class OralReadingAnalysis:
    automaticity_score: float   # 10초당 정확 음절 수
    accuracy_score: float       # 1 - (오류수 / 총음절수)
    error_count: int
    total_syllables: int
    accurate_syllables: int
    reading_time_seconds: float


def count_syllables(text: str) -> int:
    """한국어 음절 수 계산 (공백/특수문자 제외)"""
    return sum(1 for ch in text if '\uAC00' <= ch <= '\uD7A3')


def analyze_oral_reading(
    original_text: str,
    transcript: str,
    reading_time_seconds: float,
) -> OralReadingAnalysis:
    """
    원본 텍스트와 STT 변환 결과를 비교해 유창성 점수를 계산합니다.
    
    현재는 음절 수 비교 방식(단순 근사).
    추후 Levenshtein 거리 기반 정밀 오류 분류로 고도화 예정.
    """
    total_syllables = count_syllables(original_text)
    transcript_syllables = count_syllables(transcript)

    # 단순 근사: 누락된 음절 = 오류
    error_count = max(0, total_syllables - transcript_syllables)
    accurate_syllables = total_syllables - error_count

    automaticity = (accurate_syllables / reading_time_seconds) * 10 if reading_time_seconds > 0 else 0
    accuracy = accurate_syllables / total_syllables if total_syllables > 0 else 0

    return OralReadingAnalysis(
        automaticity_score=round(automaticity, 2),
        accuracy_score=round(accuracy, 4),
        error_count=error_count,
        total_syllables=total_syllables,
        accurate_syllables=accurate_syllables,
        reading_time_seconds=reading_time_seconds,
    )
