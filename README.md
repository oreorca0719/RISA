<div align="center">

# 📚 RISA
### Reading Intelligence & Skill Assessment
**초등~중학교 학습자를 위한 AI 기반 읽기 능력 진단·처방 플랫폼**

[![Frontend](https://img.shields.io/badge/Frontend-Vue.js%203-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![DB](https://img.shields.io/badge/DB-PostgreSQL%2016-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Infra](https://img.shields.io/badge/Infra-AWS-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions)](https://github.com/features/actions)

</div>

---

## 🎯 서비스 소개

RISA는 초등학교 4학년부터 6학년까지의 학습자를 대상으로 읽기 능력을 체계적으로 진단하고, 진단 결과에 기반한 맞춤 학습 처방을 제공하는 AI 기반 웹서비스입니다.

- **읽기 유창성 진단** — 음독(소리 내어 읽기) / 묵독(속으로 읽기) 측정
- **독해 이해 진단** — 사실적 / 추론적 / 비판적 이해 3층위 측정 (Claude API 채점)
- **맞춤 처방** — 독자 유형(애독자·간헐적·비독자) × 읽기 수준 매트릭스 기반 적합 도서 추천
- **리포팅** — 학생 / 학부모 / 교사 대상 맞춤 리포트 제공

---

## 🚀 배포 현황 (dev)

| 영역 | URL |
|---|---|
| **Frontend** | http://risa-frontend-dev.s3-website-ap-northeast-1.amazonaws.com |
| **Backend API** | http://risa-backend-alb-1783502255.ap-northeast-1.elb.amazonaws.com |
| **API Docs** | http://risa-backend-alb-1783502255.ap-northeast-1.elb.amazonaws.com/api/docs |

---

## 🛠 기술 스택

| 영역 | 기술 |
|---|---|
| **Frontend** | Vue.js 3 · TypeScript · Vite · Pinia · Vue Router |
| **Backend** | FastAPI (Python 3.12) · SQLAlchemy · Alembic · bcrypt · JWT |
| **Database** | PostgreSQL 16 (AWS RDS db.t3.micro) |
| **Infrastructure** | AWS S3 · ECS Fargate · ECR · ALB · RDS · CloudWatch |
| **CI/CD** | GitHub Actions (ECR push → Task Definition 자동 갱신 → ECS 배포) |
| **AI** | Anthropic Claude API (독해 채점·처방 생성·텍스트 생성, 예정) · Clova Speech STT (예정) |

---

## ✅ Sprint 0 완료 현황 (4/25~4/28)

| 이슈 | 내용 | 상태 |
|---|---|---|
| RIS-5 | [기획] GRI 25문항 라이선스 및 원문 확보 | ✅ |
| RIS-7 | [기획] 사용자 계정 구조 결정 | ✅ |
| RIS-8 | [기술] 전체 시스템 아키텍처 확정 | ✅ |
| RIS-12 | [기술] FastAPI 프로젝트 초기 구조 설정 | ✅ |
| RIS-19 | [기술] GitHub Actions CI/CD 파이프라인 구축 | ✅ |
| RIS-20 | [기술] 학생 포털 UI scaffold | ✅ |
| RIS-21 | [기술] 관리자 포털 UI scaffold | ✅ |
| RIS-22 | [기술] 회원 인증 API 구현 (JWT + PostgreSQL) | ✅ |
| RIS-23 | [기술] PostgreSQL RDS 구축 | ✅ |
| RIS-24 | [기술] 프론트엔드 라우트 가드 구현 | ✅ |
| RIS-25 | [기술] 관리자 사용자 목록 API 구현 및 UI 연동 | ✅ |

---

## ✅ Sprint 1 진행 현황 (4/28~5/11)

| 이슈 | 내용 | 상태 |
|---|---|---|
| RIS-4 | [기획] 서비스 대상 연령 범위 확정 (초4~초6) | ✅ |
| RIS-9 | [기술] PostgreSQL RDS 스키마 설계 (8개 테이블) | ✅ |
| RIS-26 | [기술] 진단 세션 API 구현 | ✅ |
| RIS-6 | [기획] 텍스트 풀 구성 방식 결정 | ⏳ 기획 확정 대기 |
| RIS-16 | [문서] 서비스 기획 제안서 초안 | ⏳ |
| RIS-17 | [문서] 사용자 시나리오 작성 | ⏳ |
| RIS-10 | [기술] STT 어댑터 레이어 설계 | ⏳ |
| RIS-11 | [기술] Clova Speech STT 파일럿 테스트 | ⏳ |
| RIS-13 | [기술] Claude API 연동 모듈 설계 | ⏳ 기획 확정 대기 |
| RIS-18 | [QA] 모듈별 QA 체크리스트 템플릿 작성 | ⏳ |

> ⚠️ **블로커**: RIS-6(텍스트 풀 구성 방식) 기획 미확정으로 인해 RIS-13(Claude API 연동), 진단 플로우 프론트 연동 전체가 대기 중.

---

## 🗂 DB 스키마 (PostgreSQL)

```
users ─┬─ user_relations     (부모-학생 연동, 추후 기능)
       ├─ diagnosis_sessions ─┬─ fluency_results       (음독/묵독 유창성)
       │         └── texts    └─ comprehension_results  (사실적/추론적/비판적 독해)
       ├─ reader_profiles     (독자 유형 분류 결과)
       ├─ prescriptions       (AI 처방 결과, DB 영구 저장)
       └─ reports             (학생/학부모/교사 리포트)
```

**texts 테이블**: 학년(elem4~elem6) × 장르(이야기글/설명글) × 수준(상/중/하) × 상태(초안/검토중/승인)

---

## 🔌 구현된 API 엔드포인트

### 인증
| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/auth/register` | 회원가입 |
| POST | `/api/auth/login` | 로그인 (JWT 발급) |
| PATCH | `/api/auth/users/{id}/name` | 이름 수정 |

### 관리자
| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/admin/users` | 역할별 사용자 목록 조회 |
| GET | `/api/admin/users/count` | 역할별 사용자 수 집계 |

### 진단
| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/diagnosis/session` | 진단 세션 생성 |
| POST | `/api/diagnosis/fluency/oral` | 음독 유창성 결과 저장 |
| POST | `/api/diagnosis/fluency/silent` | 묵독 유창성 결과 저장 |
| POST | `/api/diagnosis/comprehension` | 독해 문항 답변 저장 |
| PATCH | `/api/diagnosis/session/{id}/complete` | 세션 완료 처리 |
| GET | `/api/diagnosis/result/{session_id}` | 진단 결과 조회 |

---

## 🗂 디렉토리 구조

```
RISA/
├── frontend/                    # Vue.js 3 SPA
│   ├── src/
│   │   ├── views/
│   │   │   ├── LoginView.vue        # 로그인 (실제 API 연동)
│   │   │   ├── RegisterView.vue     # 회원가입 (실제 API 연동)
│   │   │   ├── StudentHomeView.vue  # 학생 홈 대시보드
│   │   │   ├── DiagnosisView.vue    # 진단 수행 (UI 틀, API 연동 예정)
│   │   │   ├── ResultView.vue       # 결과 열람 (UI 틀)
│   │   │   └── admin/               # 관리자 포털 5개 페이지
│   │   ├── components/
│   │   │   ├── NavBar.vue           # 학생 네비게이션
│   │   │   └── admin/AdminLayout.vue
│   │   ├── stores/auth.ts           # Pinia 인증 스토어 (JWT)
│   │   └── router/index.ts          # 라우트 가드 포함
│   └── Dockerfile
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── auth.py              # 회원 인증
│   │   │   ├── admin.py             # 관리자 API
│   │   │   └── diagnosis.py         # 진단 세션 API
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── user.py              # User 모델
│   │   │   └── core.py              # 8개 핵심 테이블 모델
│   │   └── schemas/
│   │       ├── user.py
│   │       └── diagnosis.py
│   ├── alembic/versions/
│   │   ├── 001_create_users_table.py
│   │   └── 002_add_core_schema.py   # 8개 테이블
│   ├── main.py
│   ├── start.sh                 # alembic upgrade head → uvicorn
│   └── Dockerfile
├── .github/workflows/
│   ├── frontend.yml             # S3 자동 배포
│   └── backend.yml              # ECR push → TD 자동 갱신 → ECS 배포
└── docker-compose.yml
```

---

## ⚙️ GitHub Secrets

| Secret | 값 |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM Access Key |
| `AWS_SECRET_ACCESS_KEY` | IAM Secret Key |
| `AWS_REGION` | `ap-northeast-1` |
| `S3_BUCKET_NAME` | `risa-frontend-dev` |
| `ECR_REPOSITORY` | `risa-backend` |
| `ECS_CLUSTER` | `risa-dev` |
| `ECS_SERVICE` | `risa-backend-svc` |
| `ECS_TASK_FAMILY` | `risa-backend` |
| `VITE_API_BASE_URL` | ALB URL |

---

## 🔄 CI/CD 파이프라인

```
push to main (frontend/**)
  └── npm build → S3 sync

push to main (backend/**)
  └── Docker build
      → ECR push (SHA 태그 + latest)
      → 현재 Task Definition 다운로드
      → 이미지 SHA 교체 → 새 TD 버전 자동 등록
      → ECS update-service → stable 대기
```

---

## 👥 팀

| 역할 | 이름 | 담당 |
|---|---|---|
| 기획·의사결정 | 문준석 | 서비스 기획, 교육학 도메인 |
| 설계·개발 | 김범준 | 아키텍처, 풀스택 구현 |
| 문서·QA | 최재헌 | 문서화, 테스트 |

---

<div align="center">
  <sub>경기청년 갭이어 프로젝트 · 2026</sub>
</div>
