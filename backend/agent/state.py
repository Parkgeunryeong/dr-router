"""
에이전트 State 스키마 — ★ 팀 공유 계약 (확정본)
=================================================

[개념] State = 에이전트가 들고 다니는 '메모지' 한 장(딕셔너리).
  각 노드(단계)가 이 메모지를 받아 자기 칸을 채워 다음 노드로 넘긴다.
  노드는 '바뀐 칸만' dict로 return하면 LangGraph가 알아서 병합한다.

[각 칸을 누가 채우나]
  user_input, history, location   : (입력 — API 요청에서 들어옴)
  symptoms, need_more_info        : ① 증상 수집   (박근령)
  emergency                       : ② 응급 판별   (박태준)
  departments                     : ③ 진료과 분류 (박태준, RAG는 고원영)
  hospitals                       : ④ 의료기관 검색 (최건)
  final_message                   : ⑤ 결과 안내   (박근령)

[규칙] 이 파일은 공유 계약이다. 칸을 추가/변경할 땐 반드시 팀에 공지할 것.
"""
from typing import TypedDict, List, Optional


class Department(TypedDict):
    """추천 진료과 1개의 모양"""
    name: str        # 진료과명 (예: "정형외과")
    score: float     # 적합도 0.0 ~ 1.0
    reason: str      # 이 과를 고른 한 줄 근거


class Hospital(TypedDict):
    """의료기관 1개의 모양"""
    name: str              # 병원/약국명
    dept: str              # 진료과
    distance_m: int        # 사용자로부터 거리(m)
    is_open: bool          # 현재 진료중 여부
    phone: Optional[str]   # 전화번호 (없을 수 있음)


class AgentState(TypedDict, total=False):
    # ── 입력 ──────────────────────────────
    user_input: str               # 이번 턴 사용자 발화
    history: List[dict]           # 이전 대화 [{"role":..., "content":...}, ...]
    location: dict                # {"lat": float, "lng": float}

    # ── ① 증상 수집 ───────────────────────
    symptoms: List[str]           # 추출된 핵심 증상
    need_more_info: bool          # True면 되물음(추가 질문 후 턴 종료)

    # ── ② 응급 판별 ───────────────────────
    emergency: bool               # True면 분류 건너뛰고 119 안내로 분기

    # ── ③ 진료과 분류 ─────────────────────
    departments: List[Department]  # 추천 진료과 Top-N + 근거

    # ── ④ 의료기관 검색 ───────────────────
    hospitals: List[Hospital]      # 주변 병원/약국/응급실

    # ── ⑤ 결과 ────────────────────────────
    final_message: str             # 사용자에게 보여줄 최종 메시지
