# Fitter - AI Virtual Try-On

AI 가상 피팅 서비스 PoC (Proof of Concept)

사용자가 자신의 사진을 업로드하고 의상을 선택하면 AI가 해당 옷을 입은 모습을 생성합니다.

## Status

- 무신사 메인 UI(`/musinsa`)와 피팅 플로우 UI(`/fitting`) 기본 구현됨.
- 루트 `/`는 `/musinsa`로 리다이렉트되며, 헤더 CTA로 피팅 플로우 진입.
- 데이터셋 확정에 따라 백엔드 스키마/API가 변경될 수 있습니다.
- 문서는 현재 상태와 목표 방향을 함께 기록합니다.

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

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker (for PostgreSQL)
- Poetry

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd fitter
```

2. Copy environment files (root `.env` is the source of truth)
```bash
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local
```
백엔드는 기본적으로 `backend/.env`를 읽으므로 루트 `.env`를 `backend/.env`로 복사하거나 심볼릭 링크를 만들어도 됩니다.

3. Start PostgreSQL
```bash
docker-compose up -d postgres
```

4. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

5. Setup Backend
```bash
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

## Project Structure

```
fitter/
├── frontend/          # Next.js Frontend
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
├── backend/           # FastAPI Backend
│   ├── app/
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── routers/   # API routers
│   │   └── services/  # Business logic
│   ├── alembic/       # DB migrations
│   └── tests/
├── data/              # Sample data
└── docs/              # Documentation
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clothing` | Get clothing list |
| POST | `/api/try-on` | Create try-on request |
| POST | `/api/generate-video` | Generate 360° video |
| GET | `/api/result/{id}` | Get result |

**Notes**
- ID는 문자열(opaque)이며 UUID 또는 코드형 문자열이 될 수 있습니다.
- 이미지/영상 URL은 상대/절대 경로 모두 가능하며, 프론트에서 베이스 URL을 고려해 처리합니다.

## Branch Strategy

This project uses GitHub Flow:
- `main`: Production-ready code
- `feature/*`: New features
- `fix/*`: Bug fixes
- `refactor/*`: Code refactoring
- `docs/*`: Documentation

See [CLAUDE.md](./CLAUDE.md) for more details.

## Development

### Commands

**Frontend:**
```bash
npm run dev      # Development server
npm run build    # Production build
npm run lint     # Linting
```

**Backend:**
```bash
poetry run uvicorn app.main:app --reload  # Dev server
poetry run pytest                          # Run tests
poetry run alembic upgrade head            # Run migrations
```

## Documentation

- [PRD (Product Requirements Document)](docs/PRD.md)
- [CLAUDE.md](./CLAUDE.md) - Development guidelines

## License

MIT
