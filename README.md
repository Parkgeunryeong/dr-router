# 닥터라우터 (Dr.Router)

증상을 말하면 알맞은 진료과로 **라우팅**해주는 대화형 AI 에이전트.
(자가진단이 아닌 **진료과 안내** + 주변 의료기관 안내, 응급 시 119 가드레일)

## 기술 스택
- **에이전트**: LangGraph · LangChain · LLM
- **RAG**: Chroma(Vector DB) · 한국어 임베딩
- **백엔드**: FastAPI
- **프론트**: HTML · CSS · JS (정적, FastAPI가 서빙)
- **외부 API**: 심평원 병원정보 · E-Gen(응급실·약국)

## 폴더 구조와 담당자
```
dr-router/
├── backend/
│   ├── main.py            # FastAPI 진입점 (프론트 서빙 + API)   [박근령]
│   ├── config.py          # .env 로드
│   ├── api/               # 엔드포인트 · API 계약              [최건]
│   │   ├── routes.py      #   /api/chat, /api/hospitals
│   │   └── schemas.py     #   요청/응답 Pydantic 모델 (공유 계약)
│   ├── agent/             # LangGraph 에이전트                 [박근령]
│   │   ├── graph.py       #   그래프 정의(노드 연결·분기)
│   │   ├── state.py       #   State 스키마 (★ 공유 계약)
│   │   └── nodes/         #   단계별 노드
│   │       ├── collect.py     # ① 증상 수집            [박근령]
│   │       ├── triage.py      # ② 응급도 판별           [박태준]
│   │       ├── classify.py    # ③ 진료과 분류(RAG)      [박태준]
│   │       └── search.py      # ④ 의료기관 검색(Tool)   [최건]
│   ├── rag/               # RAG                                [고원영]
│   │   ├── build_index.py #   문서→임베딩→Chroma 적재(1회)
│   │   └── retriever.py   #   검색 함수
│   ├── tools/             # 공공 API                           [최건]
│   │   ├── hira.py        #   심평원
│   │   └── egen.py        #   E-Gen
│   └── core/
│       └── emergency_rules.py  # 응급 차단 규칙              [박태준]
├── frontend/              # 웹 프론트(목업 기반)               [고원영]
├── data/                  # 질환/진료과 문서                   [고원영·박태준]
├── eval/                  # Top-3 정확도 평가                  [박태준]
└── docs/                  # 설계·산출물                        [이상현]
```

## ⚠️ 함께 건드리는 "공유 계약" 파일 (충돌 주의)
| 파일 | 소유자 | 규칙 |
|---|---|---|
| `backend/agent/state.py` | 박근령 | 맨 먼저 확정 후 동결. 바꿀 땐 팀 공지 |
| `backend/api/schemas.py` | 최건 | 박근령·최건 협의 후 변경 |
| `backend/main.py` | 박근령 | 통합 담당만 수정 |
| `requirements.txt` | 전원 | 추가만(append). 충돌 시 양쪽 다 살리기 |

## 개발 환경 세팅
```bash
# 1) 가상환경
python -m venv venv
venv\Scripts\activate         # (Windows PowerShell/cmd)
# source venv/bin/activate    # (Mac/Linux)

# 2) 패키지 설치
pip install -r requirements.txt

# 3) 환경변수
copy .env.example .env        # (Windows) / cp .env.example .env
#   .env 에 각 API 키 입력

# 4) (최초 1회) RAG 인덱스 구축
python -m backend.rag.build_index

# 5) 서버 실행
uvicorn backend.main:app --reload
#   브라우저: http://localhost:8000
```

## Git 작업 방식 (feature 브랜치 + PR)
`main` 은 항상 돌아가는 상태로 유지. **직접 push 금지**, 항상 브랜치→PR.

```bash
# 최신 main 받기
git checkout main
git pull

# 작업 브랜치 생성 (feat/<이름>-<작업>)
git checkout -b feat/taejun-rag

# 작업 후 커밋
git add .
git commit -m "feat(rag): Chroma 적재 스크립트 추가"

# 원격에 올리고 PR 생성
git push -u origin feat/taejun-rag
#   GitHub에서 Pull Request 생성 → 리뷰 → main 병합
```

**브랜치 이름 규칙**: `feat/<이름>-<작업>`, `fix/<이름>-<내용>`
**커밋 메시지**: `feat(agent): ...`, `fix(api): ...`, `docs: ...`

## 진행 원칙
> **작게 한 줄기 관통 → 기능 완성까지만.**
> 증상 입력 → 진료과 추천 → 병원 하나 표시, 이 흐름이 끝까지 돌아가면 성공.
> 정확도·확장은 시간이 남을 때만.
