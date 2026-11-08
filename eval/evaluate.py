"""
Top-3 정확도 평가 (소유자: 고원영)
testset.csv(증상→정답 진료과)에 대해 에이전트의 추천 상위 3개 안에
정답이 들어있는 비율을 측정한다.

실행: python -m eval.evaluate
"""
import csv
from pathlib import Path

from backend.agent.graph import run_agent
from backend.api.schemas import ChatRequest

TESTSET = Path("eval/testset.csv")


def top_k_departments(message: str, k: int = 3):
    res = run_agent(ChatRequest(message=message))
    return [d.name for d in res.departments[:k]]


def main():
    rows = list(csv.DictReader(TESTSET.open(encoding="utf-8")))
    hit = 0
    for r in rows:
        preds = top_k_departments(r["symptom"], k=3)
        ok = r["answer_dept"] in preds
        hit += int(ok)
        print(f"[{'O' if ok else 'X'}] {r['symptom'][:20]}... → {preds} (정답: {r['answer_dept']})")

    total = len(rows)
    acc = hit / total if total else 0
    print(f"\nTop-3 정확도: {hit}/{total} = {acc:.1%}")


if __name__ == "__main__":
    main()
