"""E-Gen 응급실·약국 API (소유자: 최건)"""
from typing import List, Dict
import requests

from backend.config import EGEN_API_KEY


def search_emergency(lat: float, lng: float) -> List[Dict]:
    """위치 기준 주변 응급실/약국을 검색해 정규화된 목록으로 반환.
    반환 형식은 hira.search_hospitals 와 동일.

    TODO: E-Gen 응급의료기관/약국 엔드포인트 호출 + 파싱
    """
    return []
