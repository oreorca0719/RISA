# RISA — 읽기 능력 진단·처방 AI 서비스

## 기술 스택

| 영역 | 기술 |
|---|---|
| Frontend | Vue.js 3 + TypeScript + Vite |
| Backend | FastAPI (Python 3.12) |
| DB | PostgreSQL 16 |
| Cache | Redis 7 |
| Infra | AWS S3, CloudFront, ECS Fargate, ECR, RDS |
| CI/CD | GitHub Actions |

---

## 로컬 개발 환경 실행

```bash
# 전체 스택 실행 (Docker 필요)
docker compose up

# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

---

## AWS 리소스 사전 세팅 (최초 1회)

### 1. S3 버킷 생성 (프론트엔드)

```bash
aws s3 mb s3://risa-frontend-dev --region ap-northeast-1

# 정적 웹사이트 호스팅 활성화
aws s3 website s3://risa-frontend-dev \
  --index-document index.html \
  --error-document index.html
```

### 2. CloudFront 배포 생성

AWS 콘솔 → CloudFront → 배포 생성
- Origin: 위에서 만든 S3 버킷
- Default root object: `index.html`
- Custom error response: 404 → `/index.html` (Vue Router 지원)

생성 후 **Distribution ID** 메모 (GitHub Secret에 등록)

### 3. ECR 리포지토리 생성 (백엔드)

```bash
aws ecr create-repository \
  --repository-name risa-backend \
  --region ap-northeast-1
```

### 4. ECS 클러스터 + 서비스 생성

```bash
# 클러스터 생성
aws ecs create-cluster --cluster-name risa-dev --region ap-northeast-1

# Task Definition은 AWS 콘솔에서 생성 권장
# (ECR 이미지 URI, 환경변수, 포트 매핑 설정)
```

---

## GitHub Secrets 등록

레포 → Settings → Secrets and variables → Actions → New repository secret

| Secret 이름 | 값 예시 | 설명 |
|---|---|---|
| `AWS_ACCESS_KEY_ID` | `AKIA...` | IAM 배포 전용 키 |
| `AWS_SECRET_ACCESS_KEY` | `...` | IAM 시크릿 |
| `AWS_REGION` | `ap-northeast-2` | 서울 리전 |
| `S3_BUCKET_NAME` | `risa-frontend-dev` | 프론트 배포 버킷 |
| `CLOUDFRONT_DISTRIBUTION_ID` | `E1ABC...` | CloudFront ID |
| `ECR_REPOSITORY` | `risa-backend` | ECR 리포지토리명 |
| `ECS_CLUSTER` | `risa-dev` | ECS 클러스터명 |
| `ECS_SERVICE` | `risa-backend-svc` | ECS 서비스명 |
| `VITE_API_BASE_URL` | `https://api.risa.dev` | 백엔드 API URL |

---

## CI/CD 동작 방식

```
PR 생성
  └── frontend/ 변경 → 빌드 + 타입체크만 (배포 X)
  └── backend/ 변경  → 빌드 + ECR 푸시만 (ECS 배포 X)

main 머지
  └── frontend/ 변경 → 빌드 → S3 업로드 → CloudFront 캐시 무효화
  └── backend/ 변경  → Docker 빌드 → ECR 푸시 → ECS 재배포 → 안정화 대기
```

---

## 디렉토리 구조

```
RISA/
├── frontend/                # Vue.js 3 SPA
│   ├── src/
│   │   ├── views/           # 페이지 컴포넌트
│   │   ├── components/      # 공통 컴포넌트
│   │   ├── router/          # Vue Router
│   │   ├── stores/          # Pinia 상태관리
│   │   └── assets/          # CSS, 이미지
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── api/endpoints/   # 라우터 (auth, diagnosis...)
│   │   ├── core/            # 설정, 보안
│   │   ├── models/          # SQLAlchemy 모델
│   │   ├── schemas/         # Pydantic 스키마
│   │   └── services/        # 비즈니스 로직
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── .github/workflows/
│   ├── frontend.yml
│   └── backend.yml
└── docker-compose.yml
```
