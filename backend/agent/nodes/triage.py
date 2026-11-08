"""② 응급도 판별 노드 (소유자: 고원영)"""
from backend.agent.state import AgentState
from backend.core.emergency_rules import is_emergency


def check_emergency(state: AgentState) -> AgentState:
    """매 입력마다 응급 신호를 먼저 검사한다.
    규칙(키워드) 기반 1차 + (확장) LLM 판단 병행 가능.
    응급이면 이후 분류를 건너뛰고 119 안내로 분기한다.
    """
    text = state.get("user_input", "")
    state["emergency"] = is_emergency(text)
    return state
