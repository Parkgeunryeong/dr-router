"""
LangGraph 그래프 정의 (소유자: 박근령)

흐름:  collect → triage →(응급?)──예──▶ [119 안내] ─▶ END
                          └──아니오──▶ classify → search → END

지금은 스켈레톤이다. 각 노드(backend/agent/nodes/)를 담당자가 구현하면
build_graph() 에서 실제 LangGraph StateGraph로 연결한다.
"""
from backend.api.schemas import ChatRequest, ChatResponse
from backend.agent.state import AgentState
from backend.agent.nodes import collect, triage, classify, search


def build_graph():
    """TODO: LangGraph StateGraph(AgentState) 구성
    from langgraph.graph import StateGraph, END
    g = StateGraph(AgentState)
    g.add_node("collect", collect.collect_symptoms)
    g.add_node("triage", triage.check_emergency)
    g.add_node("classify", classify.classify_department)
    g.add_node("search", search.search_hospitals)
    ... 조건부 엣지(응급 분기, 되물음 루프) 연결 후 g.compile()
    """
    raise NotImplementedError


def run_agent(req: ChatRequest) -> ChatResponse:
    """그래프 실행 진입점. (그래프 완성 전까지는 스텁 응답)

    완성 후에는 ChatRequest → AgentState 로 변환해 그래프를 돌리고,
    최종 AgentState → ChatResponse 로 변환해 반환한다.
    """
    # --- 임시 스텁 (프론트 연동 확인용) ---
    state: AgentState = {
        "user_input": req.message,
        "history": req.history,
        "location": {"lat": req.lat, "lng": req.lng},
    }
    # 응급 규칙만 먼저 붙여둠 (가드레일 우선)
    state = triage.check_emergency(state)
    if state.get("emergency"):
        return ChatResponse(
            reply="응급 증상이 의심됩니다. 즉시 119에 연락하거나 가까운 응급실을 방문하세요.",
            emergency=True,
        )
    return ChatResponse(
        reply="(스텁) 에이전트 연결 예정입니다. 증상을 조금 더 알려주세요.",
        need_more_info=True,
    )
