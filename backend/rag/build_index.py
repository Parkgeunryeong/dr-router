"""
RAG 인덱스 구축 (소유자: 박태준) — 최초 1회 실행
data/departments/*.md (진료과 요약 문서) → 임베딩 → Chroma 적재

실행: python -m backend.rag.build_index
"""
from pathlib import Path

DATA_DIR = Path("data/departments")


def main():
    docs = sorted(DATA_DIR.glob("*.md"))
    print(f"[build_index] 문서 {len(docs)}개 발견")

    # TODO:
    #   import chromadb
    #   client = chromadb.PersistentClient(path="backend/rag/chroma_db")
    #   col = client.get_or_create_collection("departments")
    #   각 문서를 읽어 임베딩 후 col.add(...)
    #   (문서 수가 적으므로 통째로 넣어도 충분)
    print("[build_index] TODO: 임베딩 후 Chroma 적재")


if __name__ == "__main__":
    main()
