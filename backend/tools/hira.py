"""심평원 병원정보 OpenAPI (소유자: 최건)"""
import logging
import time
from typing import Dict, List, Tuple

from backend.config import HIRA_API_KEY
from backend.tools._common import fetch_items, haversine_m

logger = logging.getLogger(__name__)

# 병원기본목록. xPos(경도)/yPos(위도)/radius(m)를 주면 반경 검색이 되고
# 응답에 distance(m)가 붙는다. (실제 호출로 확인)
BASE = "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

# 진료과목코드(dgsbjtCd). 서울 의원 간판명과 대조해 실측 검증한 값.
DGSBJT = {
    "내과": "01", "신경과": "02", "정신건강의학과": "03", "외과": "04",
    "정형외과": "05", "신경외과": "06", "심장혈관흉부외과": "07", "성형외과": "08",
    "마취통증의학과": "09", "산부인과": "10", "소아청소년과": "11", "안과": "12",
    "이비인후과": "13", "피부과": "14", "비뇨의학과": "15", "영상의학과": "16",
    "재활의학과": "21", "가정의학과": "23",
}
# 옛 이름·줄임말 → 표준 진료과명
ALIASES = {
    "정신과": "정신건강의학과", "흉부외과": "심장혈관흉부외과", "소아과": "소아청소년과",
    "비뇨기과": "비뇨의학과", "통증의학과": "마취통증의학과",
}

# 이 API는 반경 검색 한 번에 3~8초가 걸리고 결과가 거리순이 아니다(실측).
# 그래서 여러 번 나눠 부르지 않고, 한 번에 넉넉히 받아 직접 정렬한다.
# 도심은 2km로 충분하고, 모자랄 때만 20km로 한 번 더 부른다.
RADII = (2000, 20000)
ROWS = 500
TIMEOUT = 15

_CACHE_TTL = 10 * 60  # 같은 위치·진료과 재검색은 10분간 캐시 (병원 목록은 거의 안 바뀜)
_cache: Dict[Tuple, Tuple[float, List[Dict]]] = {}


def search_hospitals(dept: str, lat: float, lng: float, top: int = 5) -> List[Dict]:
    """진료과 + 위치로 주변 병원을 가까운 순으로 반환.

    반환 형식(= schemas.HospitalOut):
      {"name","dept","distance_m","is_open","phone"}
    지원하지 않는 진료과이거나 API 호출에 실패하면 빈 리스트.
    """
    dept = ALIASES.get(dept, dept)
    code = DGSBJT.get(dept)
    if code is None:
        logger.warning("진료과목코드를 모르는 진료과: %s", dept)
        return []
    if lat is None or lng is None:
        return []

    cache_key = (code, round(lat, 3), round(lng, 3))  # 소수 3자리 ≈ 100m
    cached = _cache.get(cache_key)
    if cached and time.time() - cached[0] < _CACHE_TTL:
        return cached[1][:top]

    out: List[Dict] = []
    for radius in RADII:
        items = fetch_items(BASE, HIRA_API_KEY, {
            "pageNo": 1, "numOfRows": ROWS,
            "xPos": lng, "yPos": lat, "radius": radius,
            "dgsbjtCd": code,
        }, timeout=TIMEOUT)
        if len(items) >= ROWS:
            logger.warning("반경 %sm 안에 %s 병원이 %s곳 이상 — 가장 가까운 곳이 빠졌을 수 있음", radius, dept, ROWS)
        out = [h for h in (_normalize(it, dept, lat, lng) for it in items) if h]
        if len(out) >= top:
            break

    out.sort(key=lambda h: h["distance_m"])
    if out:  # 실패(빈 결과)는 캐시하지 않고 다음 호출 때 다시 시도
        _cache[cache_key] = (time.time(), out)
    return out[:top]


def _normalize(it: Dict, dept: str, lat: float, lng: float):
    try:
        distance = int(float(it["distance"]))
    except (KeyError, TypeError, ValueError):
        distance = haversine_m(lat, lng, it.get("YPos"), it.get("XPos"))
    if distance is None:
        return None
    return {
        "name": it.get("yadmNm", ""),
        "dept": dept,
        "distance_m": distance,
        "is_open": True,  # 병원기본목록에는 운영시간이 없음 → 우선 True (팀 협의 필요)
        "phone": it.get("telno") or None,
    }
