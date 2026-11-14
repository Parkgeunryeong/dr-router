"""E-Gen 응급의료기관 API (소유자: 최건)"""
import time
from typing import Dict, List

from backend.config import EGEN_API_KEY
from backend.tools._common import fetch_items, haversine_m

# 응급의료기관 목록. 조건 없이 부르면 전국(약 530곳)이 좌표와 함께 온다.
# 좌표로 응급실만 골라주는 오퍼레이션은 없어서(getEgytLcinfoInqire는 일반
# 병원까지 섞여 옴), 전국 목록을 받아 직접 거리를 계산한다. (실제 호출로 확인)
ER_LIST = "https://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire"

_CACHE_TTL = 6 * 60 * 60  # 응급실 목록은 거의 안 바뀌므로 6시간 캐시
_cache: Dict = {"at": 0.0, "items": []}


def _er_list() -> List[Dict]:
    if _cache["items"] and time.time() - _cache["at"] < _CACHE_TTL:
        return _cache["items"]
    items = fetch_items(ER_LIST, EGEN_API_KEY, {"pageNo": 1, "numOfRows": 1000}, timeout=10)
    if items:  # 실패(빈 결과)는 캐시하지 않고 다음 호출 때 다시 시도
        _cache.update(at=time.time(), items=items)
    return items


def search_emergency(lat: float, lng: float, top: int = 3) -> List[Dict]:
    """위치 기준 가까운 응급실을 가까운 순으로 반환.
    반환 형식은 hira.search_hospitals 와 동일.
    """
    if lat is None or lng is None:
        return []

    out = []
    for it in _er_list():
        distance = haversine_m(lat, lng, it.get("wgs84Lat"), it.get("wgs84Lon"))
        if distance is None:
            continue
        out.append({
            "name": it.get("dutyName", ""),
            "dept": "응급의학과",
            "distance_m": distance,
            "is_open": True,  # 응급실은 24시간 운영
            "phone": it.get("dutyTel3") or it.get("dutyTel1") or None,  # Tel3 = 응급실 직통
        })

    out.sort(key=lambda h: h["distance_m"])
    return out[:top]
