"""③ 진료과 분류 노드 (소유자: 고원영)"""
from backend.agent.state import AgentState
from backend.rag.retriever import retrieve


def classify_department(state: AgentState) -> AgentState:
    """RAG로 검색한 진료과·질환 문서를 근거로 적합한 진료과를 추론한다.
    여러 과에 걸칠 수 있으므로 상위 후보(Top-N)와 근거를 함께 담는다.
    """
    symptoms = state.get("symptoms", [])
    query = " ".join(symptoms) or state.get("user_input", "")

    docs = retrieve(query, k=3)  # 근거 문서 (박태준의 retriever)

    # TODO: LLM에 (증상 + docs)를 주고 Top-N 진료과 + 근거 생성
    state["departments"] = []  # [{"name","score","reason"}, ...]
    return state
