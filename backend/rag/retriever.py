"""RAG 검색 (소유자: 박태준)"""
from typing import List, Dict


def retrieve(query: str, k: int = 3) -> List[Dict]:
    """증상 쿼리로 관련 진료과/질환 문서 Top-k를 검색한다.

    TODO:
      import chromadb
      client = chromadb.PersistentClient(path=CHROMA_DIR)
      col = client.get_collection("departments")
      res = col.query(query_texts=[query], n_results=k)
      → [{"text":..., "dept":..., "source":...}, ...] 형태로 반환
    """
    return []
