"""
에이전트 State 스키마 — ★ 팀 공유 계약 (소유자: 박근령)
모든 노드가 이 State를 읽고/채워서 다음 노드로 넘긴다.
바꿀 때는 반드시 팀에 공지할 것.
"""
from typing import TypedDict, List, Optional


class Department(TypedDict):
    name: str        # 진료과명 (예: "외과")
    score: float     # 적합도 0~1
    reason: str      # 선택 근거


class Hospital(TypedDict):
    name: str
    dept: str
    distance_m: int
    is_open: bool
    phone: Optional[str]


class AgentState(TypedDict, total=False):
    # 입력
    user_input: str                 # 이번 턴 사용자 발화
    history: List[dict]             # 이전 대화 (role/content)

    # ① 증상 수집
    symptoms: List[str]
    need_more_info: bool            # True면 되물음 루프

    # ② 응급도 판별
    emergency: bool

    # ③ 진료과 분류
    departments: List[Department]   # Top-N 후보 + 근거

    # ④ 의료기관 검색
    location: dict                  # {"lat": float, "lng": float}
    hospitals: List[Hospital]

    # ⑤ 결과
    final_message: str
