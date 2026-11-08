"""① 증상 수집 노드 (소유자: 박근령)"""
from backend.agent.state import AgentState


def collect_symptoms(state: AgentState) -> AgentState:
    """자연어 입력에서 핵심 증상을 추출한다.
    정보가 부족하면 state["need_more_info"] = True 로 두어 되물음 루프를 돈다.
    (Memory: state["history"] 활용)
    """
    # TODO: LLM으로 증상 추출 + 충분성 판단
    state.setdefault("symptoms", [])
    state["need_more_info"] = False
    return state
