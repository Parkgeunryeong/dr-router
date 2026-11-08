"""API 엔드포인트 (소유자: 최건)"""
from fastapi import APIRouter

from backend.api.schemas import ChatRequest, ChatResponse
from backend.agent.graph import run_agent

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """증상 입력 → 에이전트 실행 → 진료과/병원 안내 반환"""
    return run_agent(req)
