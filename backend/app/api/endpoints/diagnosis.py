from fastapi import APIRouter

router = APIRouter()


@router.post("/session")
async def create_session():
    # TODO: 진단 세션 생성
    return {"message": "not implemented"}


@router.post("/fluency/oral")
async def submit_oral_fluency():
    # TODO: 음독 유창성 측정 (STT 연동)
    return {"message": "not implemented"}


@router.post("/fluency/silent")
async def submit_silent_fluency():
    # TODO: 묵독 유창성 측정
    return {"message": "not implemented"}


@router.post("/comprehension")
async def submit_comprehension():
    # TODO: 독해 이해 문항 채점 (사실적/추론적/비판적)
    return {"message": "not implemented"}


@router.get("/result/{session_id}")
async def get_result(session_id: str):
    # TODO: 진단 결과 조회
    return {"message": "not implemented", "session_id": session_id}
