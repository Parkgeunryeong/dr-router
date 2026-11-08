"""
API 요청/응답 모델 — ★ 프론트↔백엔드 공유 계약 (소유자: 최건)
프론트의 fetch 본문/응답이 이 모델과 일치해야 한다.
"""
from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    history: List[dict] = []


class DepartmentOut(BaseModel):
    name: str
    score: float
    reason: str


class HospitalOut(BaseModel):
    name: str
    dept: str
    distance_m: int
    is_open: bool
    phone: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str                              # 사용자에게 보여줄 메시지
    emergency: bool = False                 # 응급이면 True → 프론트에서 119 안내
    need_more_info: bool = False            # True면 되묻는 중
    departments: List[DepartmentOut] = []   # 추천 진료과 (Top-N)
    hospitals: List[HospitalOut] = []       # 주변 의료기관
