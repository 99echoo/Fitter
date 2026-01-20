# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Fitter** - AI Virtual Try-On 데모 서비스

무신사 메인 페이지에 통합 가능한 AI 가상 피팅 서비스 PoC. 사용자가 자신의 사진을 업로드하고 의상을 선택하면 AI가 해당 옷을 입은 모습을 생성합니다.

## Current Status

- UI는 아직 미구현 상태이며, 데이터셋 확정에 따라 백엔드 스키마/API가 변경될 수 있습니다.
- 문서는 현재 상태와 목표 방향을 함께 기록합니다.
- ID는 문자열(opaque)로 취급하며 UUID/코드형 문자열 모두 허용합니다.

## Tech Stack

### Frontend
- Next.js 16.x (App Router)
- TypeScript
- Tailwind CSS
- Shadcn/ui

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL
- SQLAlchemy + Alembic

### AI/ML
- Google Nano Banana Pro (이미지 생성/편집)
- Kling AI 2.1 (Image-to-Video)

## Project Structure

```
fitter/
├── frontend/          # Next.js 프론트엔드
│   ├── src/app/       # App Router 페이지
│   ├── src/components/
│   └── src/lib/
├── backend/           # FastAPI 백엔드
│   ├── app/
│   │   ├── models/    # SQLAlchemy 모델
│   │   ├── schemas/   # Pydantic 스키마
│   │   ├── routers/   # API 라우터
│   │   └── services/  # 비즈니스 로직 (AI 연동)
│   └── alembic/       # DB 마이그레이션
├── data/              # 샘플 데이터
└── docs/              # 문서 (PRD 포함)
```

## Commands

### Frontend
```bash
cd frontend
npm install              # 의존성 설치
npm run dev              # 개발 서버 (localhost:3000)
npm run build            # 프로덕션 빌드
npm run lint             # ESLint 실행
```

### Backend
```bash
cd backend
poetry install           # 의존성 설치
poetry run uvicorn app.main:app --reload  # 개발 서버 (localhost:8000)
poetry run alembic upgrade head           # DB 마이그레이션 실행
poetry run pytest        # 테스트 실행
```
루트 `.env`를 기준으로 사용하며, 필요 시 `backend/.env`로 복사 또는 심볼릭 링크를 사용합니다.

### Database
```bash
# Docker로 PostgreSQL 실행
docker-compose up -d postgres

# 마이그레이션 생성
cd backend
poetry run alembic revision --autogenerate -m "description"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clothing` | 의상 목록 조회 |
| POST | `/api/try-on` | 가상 피팅 요청 |
| POST | `/api/generate-video` | 360도 영상 생성 |
| GET | `/api/result/{id}` | 결과 조회 |

**Notes**
- ID는 문자열(opaque)이며 UUID 또는 코드형 문자열이 될 수 있습니다.
- 이미지/영상 URL은 상대/절대 경로 모두 가능하며, 프론트에서 베이스 URL을 고려해 처리합니다.

## Database Schema

### clothing 테이블
- id (string), name, category, image_url, brand, price

### try_on_request 테이블
- id (string), clothing_id (string), face_image_path, body_image_path, status, result_image_url, video_url

## AI Integration

### Nano Banana Pro (Virtual Try-On)
- 모델: `gemini-2.0-flash-exp-image-generation` (현재 기준, 데이터셋/정책에 따라 변경 가능)
- SDK: `google-genai`
- 입력: 얼굴 사진 + 전신 사진 + 의상 이미지
- 출력: 1024x1024 합성 이미지

### Kling AI (360도 영상)
- 모델: Kling 2.1 (Image-to-Video)
- 입력: 합성 이미지
- 출력: 5초, 720p 영상

## Environment Variables

```env
# Backend (root .env)
DATABASE_URL=postgresql://fitter:fitter_password@localhost:5432/fitter
GOOGLE_API_KEY=your_google_api_key_here
KLING_API_KEY=your_kling_api_key_here

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development Guidelines

### 코드 스타일
- Python: PEP 8, Black formatter
- TypeScript: ESLint + Prettier
- 커밋 메시지: Conventional Commits (feat:, fix:, docs:, etc.)

### 파일 네이밍
- Python: snake_case
- TypeScript/React: PascalCase (컴포넌트), camelCase (함수/변수)

### API 응답 형식
별도 래퍼 없이 엔드포인트 스키마 그대로 JSON을 반환합니다.

## Key Files

- `backend/app/services/nano_banana.py` - Nano Banana Pro API 연동
- `backend/app/services/kling_ai.py` - Kling AI API 연동
- `frontend/src/components/fitting/ImageUploader.tsx` - 이미지 업로드 컴포넌트
- `frontend/src/components/fitting/ResultViewer.tsx` - 결과 뷰어 컴포넌트

## Branch Strategy (GitHub Flow)

### Branch Types
| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New feature development | `feature/frontend-image-uploader` |
| `fix/` | Bug fixes | `fix/backend-cors-error` |
| `refactor/` | Code refactoring | `refactor/api-response-format` |
| `docs/` | Documentation | `docs/api-documentation` |

### Workflow
1. Create feature branch from `main`
2. Develop and commit changes
3. Create Pull Request
4. Code review (self-review allowed)
5. Squash and merge to `main`

### Commit Convention
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Example: `feat: add image upload component`

## Related Documentation

- [PRD (Product Requirements Document)](docs/PRD.md)
- [Google Nano Banana Pro Docs](https://ai.google.dev/gemini-api/docs/image-generation)
- [Kling AI API Docs](https://app.klingai.com/global/dev/document-api)
