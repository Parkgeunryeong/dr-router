"""
FastAPI 진입점 (소유자: 박근령)
- /api/* : 백엔드 API
- /      : frontend/ 정적 파일 서빙
실행: uvicorn backend.main:app --reload  →  http://localhost:8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router

app = FastAPI(title="Dr.Router")

# 개발 편의를 위해 CORS 허용 (배포 시 도메인 제한 권장)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터
app.include_router(router, prefix="/api")

# 프론트엔드 정적 서빙 (반드시 라우터 등록 이후, 맨 마지막에 mount)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
