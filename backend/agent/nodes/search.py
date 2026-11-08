"""④ 의료기관 검색 노드 (소유자: 최건)"""
from backend.agent.state import AgentState
from backend.tools import hira, egen


def search_hospitals(state: AgentState) -> AgentState:
    """분류된 진료과 + 사용자 위치로 공공 API를 호출해 병원/약국/응급실을 찾는다."""
    depts = state.get("departments", [])
    loc = state.get("location", {}) or {}
    top_dept = depts[0]["name"] if depts else None

    hospitals = []
    if top_dept and loc.get("lat") and loc.get("lng"):
        hospitals += hira.search_hospitals(top_dept, loc["lat"], loc["lng"])
        hospitals += egen.search_emergency(loc["lat"], loc["lng"])

    state["hospitals"] = hospitals
    return state
