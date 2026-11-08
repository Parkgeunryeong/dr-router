"""심평원 병원정보 OpenAPI (소유자: 최건)"""
from typing import List, Dict
import requests

from backend.config import HIRA_API_KEY


def search_hospitals(dept: str, lat: float, lng: float) -> List[Dict]:
    """진료과 + 위치로 주변 병원을 검색해 정규화된 목록으로 반환.

    반환 형식(= schemas.HospitalOut):
      {"name","dept","distance_m","is_open","phone"}

    TODO: 심평원 병원정보서비스 엔드포인트 호출 + 파싱 + 거리 계산
    """
    return []
