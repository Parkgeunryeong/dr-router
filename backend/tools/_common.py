"""공공데이터포털 OpenAPI 공통 호출 헬퍼 (소유자: 최건)"""
import logging
from math import asin, cos, radians, sin, sqrt
from typing import Dict, List, Optional
from urllib.parse import unquote

import requests

logger = logging.getLogger(__name__)


def haversine_m(lat1: float, lng1: float, lat2, lng2) -> Optional[int]:
    """두 좌표 사이 거리(m). 상대 좌표가 없거나 숫자가 아니면 None."""
    try:
        lat2, lng2 = float(lat2), float(lng2)
    except (TypeError, ValueError):
        return None
    if not lat2 or not lng2:
        return None
    dlat, dlng = radians(lat2 - lat1), radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return int(2 * 6371000 * asin(sqrt(a)))


def fetch_items(url: str, key: str, params: Dict, timeout: float = 5) -> List[Dict]:
    """OpenAPI를 호출해 response.body.items.item 을 항상 list로 돌려준다.

    외부 API가 막히거나 느려도 데모가 멈추지 않도록, 실패하면 예외 대신
    빈 리스트를 반환하고 원인만 로그로 남긴다. 인증키는 로그에 남기지 않는다.
    """
    if not key:
        logger.warning("API 키가 비어 있음 (.env 확인): %s", url)
        return []
    # Decoding 키에는 '%'가 없다. '%'가 있으면 Encoding 키를 넣은 것이므로
    # 풀어서 쓴다 (그대로 params로 넘기면 이중 인코딩되어 인증 실패).
    if "%" in key:
        key = unquote(key)

    try:
        r = requests.get(url, params={"serviceKey": key, "_type": "json", **params}, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        # 예외 메시지에는 serviceKey가 포함된 URL이 들어가므로 종류만 남긴다
        logger.warning("API 호출 실패 (%s): %s", type(e).__name__, url)
        return []
    except ValueError:
        logger.warning("API가 JSON이 아닌 응답을 반환: %s", url)
        return []

    response = data.get("response") or {}
    header = response.get("header") or {}
    if header.get("resultCode") != "00":
        logger.warning("API 오류 응답 (%s %s): %s", header.get("resultCode"), header.get("resultMsg"), url)
        return []

    items = (response.get("body") or {}).get("items") or {}
    items = items.get("item", []) if isinstance(items, dict) else []
    return [items] if isinstance(items, dict) else items  # 1건이면 dict로 옴
