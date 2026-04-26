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

RISA는 초등학교 저학년부터 중학교 1학년까지의 학습자를 대상으로 읽기 능력을 체계적으로 진단하고, 진단 결과에 기반한 맞춤 학습 처방을 제공하는 AI 기반 웹서비스입니다.

- **읽기 유창성 진단** — 음독(소리 내어 읽기) / 묵독(속으로 읽기) 자동 측정
- **독해 이해 진단** — 사실적 / 추론적 / 비판적 이해 3층위 측정
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
| **CI/CD** | GitHub Actions |
| **AI** | Anthropic Claude API (예정) · Clova Speech STT (예정) |

---

## ✅ Sprint 0 완료 현황 (4/25~4/28)

| 이슈 | 내용 | 상태 |
|---|---|---|
| RIS-5 | [기획] GRI 25문항 라이선스 및 원문 확보 | ✅ 완료 |
| RIS-7 | [기획] 사용자 계정 구조 결정 | ✅ 완료 |
| RIS-8 | [기술] 전체 시스템 아키텍처 확정 | ✅ 완료 |
| RIS-9 | [기술] PostgreSQL RDS 스키마 설계 | 🔜 Sprint 1 |
| RIS-12 | [기술] FastAPI 프로젝트 초기 구조 설정 | ✅ 완료 |
| RIS-19 | [기술] GitHub Actions CI/CD 파이프라인 구축 | ✅ 완료 |
| RIS-20 | [기술] 학생 포털 UI scaffold | ✅ 완료 |
| RIS-21 | [기술] 관리자 포털 UI scaffold | ✅ 완료 |
| RIS-22 | [기술] 회원 인증 API 구현 (JWT + PostgreSQL) | ✅ 완료 |
| RIS-23 | [기술] PostgreSQL RDS 구축 | ✅ 완료 |
| RIS-24 | [기술] 프론트엔드 라우트 가드 구현 | ✅ 완료 |

---

## 🗂 디렉토리 구조

```
RISA/
├── frontend/                    # Vue.js 3 SPA
│   ├── src/
│   │   ├── views/
│   │   │   ├── LoginView.vue        # 로그인
│   │   │   ├── RegisterView.vue     # 회원가입
│   │   │   ├── StudentHomeView.vue  # 학생 홈
│   │   │   ├── DiagnosisView.vue    # 진단 수행
│   │   │   ├── ResultView.vue       # 결과 열람
│   │   │   └── admin/               # 관리자 포털 (5개 페이지)
│   │   ├── components/
│   │   │   ├── NavBar.vue           # 학생 네비게이션
│   │   │   └── admin/AdminLayout.vue # 관리자 사이드바 레이아웃
│   │   ├── stores/
│   │   │   └── auth.ts              # Pinia 인증 스토어 (JWT)
│   │   └── router/index.ts          # 라우트 가드 포함
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── auth.py              # 회원가입·로그인·이름수정
│   │   │   └── diagnosis.py         # 진단 (skeleton)
│   │   ├── core/
│   │   │   ├── config.py            # 환경변수 설정
│   │   │   ├── database.py          # AsyncSession 설정
│   │   │   └── security.py          # bcrypt·JWT
│   │   ├── models/user.py           # User SQLAlchemy 모델
│   │   ├── schemas/user.py          # Pydantic 스키마
│   │   └── services/user_service.py # 회원 비즈니스 로직
│   ├── alembic/
│   │   └── versions/001_create_users_table.py
│   ├── main.py
│   ├── start.sh                 # 마이그레이션 → uvicorn 시작
│   ├── requirements.txt
│   └── Dockerfile
├── .github/workflows/
│   ├── frontend.yml             # S3 자동 배포
│   └── backend.yml              # ECR → ECS 자동 배포
└── docker-compose.yml           # 로컬 개발 환경
```

---

## 🖥 로컬 개발 환경 실행

```bash
# 전체 스택 실행 (Docker 필요)
docker compose up

# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

---

## ⚙️ GitHub Secrets 등록

| Secret | 설명 |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM Access Key |
| `AWS_SECRET_ACCESS_KEY` | IAM Secret Key |
| `AWS_REGION` | `ap-northeast-1` |
| `S3_BUCKET_NAME` | 프론트 S3 버킷명 |
| `ECR_REPOSITORY` | ECR 리포지토리명 |
| `ECS_CLUSTER` | ECS 클러스터명 |
| `ECS_SERVICE` | ECS 서비스명 |
| `ECS_TASK_FAMILY` | ECS Task Definition 패밀리명 |
| `VITE_API_BASE_URL` | 백엔드 ALB URL |

---

## 🔄 CI/CD 파이프라인

```
push to main (frontend/**)
  └── npm install → type-check → build → S3 sync

push to main (backend/**)
  └── Docker build → ECR push → ECS update-service (최신 Task Definition) → stable 대기
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
