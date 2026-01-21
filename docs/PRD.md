# AI 피팅 서비스 PRD (Product Requirements Document)

## 1. 프로젝트 개요

### 1.1 프로젝트명
**Fitter** - AI Virtual Try-On 데모 서비스

### 1.2 목적
무신사 메인 페이지에 통합 가능한 AI 가상 피팅 서비스 PoC(Proof of Concept) 개발

### 1.3 대상 사용자
- 온라인 쇼핑 시 옷이 자신에게 어울리는지 확인하고 싶은 사용자
- 구매 전 가상으로 착용해보고 싶은 사용자

### 1.4 핵심 가치
- 사용자 경험 향상: 구매 전 가상 착용으로 만족도 증가
- 판매 전환율 증대: 시각적 확신을 통한 구매 결정 촉진
- 반품률 감소: 사전 확인을 통한 미스매치 방지

### 1.5 현재 상태 및 전제
- 무신사 스타일 메인 페이지 및 피팅 플로우 UI 기본 구현됨(라우팅: `/`→`/musinsa`, `/fitting`).
- 현재 UI 플로우: 시작 화면 → 의상 선택 → 얼굴/전신 업로드 → 대기 → 결과 확인.
- 데이터셋 확정 전이므로 스키마/API 변경 가능성이 있습니다.
- ID는 문자열(opaque)로 취급하며 UUID 또는 코드형 문자열 모두 허용합니다.
- API 응답은 엔드포인트 스키마 그대로 반환하며 별도 래퍼는 사용하지 않습니다.
- 이미지/영상 URL은 상대 또는 절대 경로를 허용하며, 프론트에서 베이스 URL을 고려해 처리합니다.

---

## 2. 기능 요구사항

### 2.1 핵심 기능 (MVP)

#### F1. 메인 페이지 통합
- 무신사 스타일 메인 페이지 UI 클론
- "AI 피팅룸" 진입 버튼 배치
- 버튼 클릭 시 피팅 서비스 페이지로 이동

#### F2. 사진 업로드
- **얼굴 사진 업로드**: 고화질 얼굴 합성용
- **전신 사진 업로드**: 정면 자세의 전신 이미지
- 지원 포맷: JPG, PNG, WebP
- 최대 파일 크기: 10MB
- 업로드 가이드라인 안내 (정면, 밝은 조명, 전신 보이기 등)

#### F3. 의상 선택
- 사전 준비된 의류 목록에서 선택
- 카테고리: 상의, 하의, 아우터, 원피스 (데이터셋에 따라 변동 가능)
- 썸네일 + 제품명 표시
- 5-10개 샘플 의상 제공

#### F4. AI 가상 착용 이미지 생성
- OpenAI GPT-Image 1.5 모델 활용
- 입력: 얼굴 사진 + 전신 사진 + 의상 이미지 (최대 5장)
- 출력: 사용자가 해당 옷을 입은 합성 이미지
- 해상도: 1024x1536 (기본값, `OPENAI_IMAGE_OUTPUT_SIZE`로 변경 가능)
- 일관된 정면 포즈 유지

#### F5. 360도 회전 영상 생성
- Kling AI 모델 활용 (Image-to-Video)
- 입력: 생성된 합성 이미지
- 출력: 5초, 720p 회전 영상
- 포맷: MP4 또는 GIF

#### F6. 결과 제공
- 합성 이미지 화면 표시
- 회전 영상 재생
- 다운로드 기능 (이미지/영상)

### 2.2 부가 기능

#### F7. 샘플 모델 사진 제공
- 사용자가 자신의 사진이 없을 경우 샘플 모델 사진 선택 가능
- 2-3개의 다양한 체형/성별 샘플 제공

#### F8. Before/After 비교
- 원본 사진과 합성 결과 좌우 비교 뷰

---

## 3. 기술 스택

### 3.1 프론트엔드
| 기술 | 용도 |
|------|------|
| Next.js 16.x | React 프레임워크, SSR/SSG |
| TypeScript | 타입 안정성 |
| Tailwind CSS | 스타일링 |
| Shadcn/ui | UI 컴포넌트 |

### 3.2 백엔드
| 기술 | 용도 |
|------|------|
| FastAPI | Python REST API 서버 |
| Python 3.11+ | 런타임 |
| Pydantic | 데이터 검증 |
| PostgreSQL | 관계형 데이터베이스 |
| SQLAlchemy | ORM |
| Alembic | DB 마이그레이션 |

### 3.3 AI/ML
| 기술 | 용도 |
|------|------|
| OpenAI GPT-Image 1.5 | 이미지 생성/편집 (Virtual Try-On) |
| Kling AI 2.1 | Image-to-Video (360도 영상) |
| openai SDK | GPT-Image API 연동 |

- 현재 모델 ID: `gpt-image-1.5` (환경 변수 `OPENAI_IMAGE_MODEL`로 변경 가능)

### 3.4 인프라 (예정)
| 기술 | 용도 |
|------|------|
| Docker | 컨테이너화 |
| AWS S3 | 이미지/영상 스토리지 |
| Vercel | 프론트엔드 배포 (옵션) |

---

## 4. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Next.js)                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ 메인    │  │ 업로드  │  │ 의상    │  │ 결과    │        │
│  │ 페이지  │→ │ 페이지  │→ │ 선택    │→ │ 페이지  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Upload      │  │ Try-On      │  │ Video       │         │
│  │ Handler     │  │ Service     │  │ Service     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└───────┬───────────────┬─────────────┬───────────────────────┘
        │               │             │
        ▼               ▼             ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ PostgreSQL    │ │ GPT-Image     │ │ Kling AI      │
│ Database      │ │ Pro API       │ │ API           │
└───────────────┘ └───────────────┘ └───────────────┘
        │
        ▼
┌───────────────┐
│ File Storage  │
│ (Local/S3)    │
└───────────────┘
```

---

## 5. API 설계

※ 모든 ID는 문자열(opaque)이며 UUID 또는 코드형 문자열이 될 수 있습니다.

### 5.1 의상 목록 조회
```
GET /api/clothing

Response:
{
  "items": [
    {
      "id": "item_001",
      "name": "오버핏 데님 자켓",
      "category": "아우터",
      "image_url": "/images/clothing/jacket_001.png",
      "brand": "Sample Brand",
      "price": 89000
    }
  ]
}
```

### 5.2 가상 피팅 요청
```
POST /api/try-on

Request (multipart/form-data):
- face_image: File (얼굴 사진)
- body_image: File (전신 사진)
- clothing_ids: string[] (의상 ID 배열, opaque)

Response:
{
  "request_id": "req_abc123",
  "status": "pending" | "processing" | "completed" | "failed",
  "result_image_url": "https://...",
  "clothing_items": [
    { "id": "item_001", "category": "상의", "name": "..." }
  ],
  "created_at": "2026-01-20T12:00:00Z"
}
```

Notes:
- 카테고리별 1개씩만 선택 가능하며 중복 카테고리는 거부됩니다.

### 5.3 360도 영상 생성
```
POST /api/generate-video

Request:
{
  "request_id": "req_abc123"  // 또는 result_image_url
}

Response:
{
  "video_id": "vid_xyz789",
  "status": "processing" | "completed" | "failed",
  "video_url": "https://...",
  "duration": 5,
  "resolution": "720p"
}
```

### 5.4 결과 조회
```
GET /api/result/{request_id}

Response:
{
  "request_id": "req_abc123",
  "status": "pending" | "processing" | "completed" | "failed",
  "result_image_url": "https://...",
  "video_url": "https://...",
  "error_message": null,
  "clothing_items": [
    { "id": "item_001", "category": "상의", "name": "..." }
  ],
  "created_at": "2026-01-20T12:00:00Z",
  "completed_at": "2026-01-20T12:01:00Z"
}
```

---

## 6. 데이터베이스 설계

### 6.1 ERD (Entity Relationship Diagram)

```
┌─────────────────────┐       ┌─────────────────────┐
│      clothing       │       │   try_on_request    │
├─────────────────────┤       ├─────────────────────┤
│ id (PK, STRING)     │       │ id (PK, STRING)     │
│ name (VARCHAR)      │◄──────│ clothing_id (FK, STRING) │
│ category (ENUM)     │       │ face_image_path     │
│ image_url (VARCHAR) │       │ body_image_path     │
│ brand (VARCHAR)     │       │ status (ENUM)       │
│ price (INTEGER)     │       │ clothing_items (JSON) │
│ description (TEXT)  │       │ result_image_url    │
│ created_at          │       │ video_url           │
│ updated_at          │       │ error_message       │
└─────────────────────┘       │ created_at          │
                              │ updated_at          │
                              │ completed_at        │
                              └─────────────────────┘
```

### 6.2 테이블 스키마

※ ID는 데이터셋에 따라 UUID 또는 코드형 문자열을 사용합니다. 아래 예시는 문자열 기준입니다.

#### clothing 테이블
```sql
CREATE TABLE clothing (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('상의', '하의', '아우터', '원피스')),
    image_url VARCHAR(500) NOT NULL,
    brand VARCHAR(100),
    price INTEGER DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clothing_category ON clothing(category);
```

#### try_on_request 테이블
```sql
CREATE TABLE try_on_request (
    id VARCHAR(64) PRIMARY KEY,
    clothing_id VARCHAR(64) NOT NULL REFERENCES clothing(id),
    clothing_items JSON,
    face_image_path VARCHAR(500) NOT NULL,
    body_image_path VARCHAR(500) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    result_image_url VARCHAR(500),
    video_url VARCHAR(500),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_try_on_request_status ON try_on_request(status);
CREATE INDEX idx_try_on_request_created_at ON try_on_request(created_at);
```

### 6.3 SQLAlchemy 모델

```python
# models/clothing.py
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class Clothing(Base):
    __tablename__ = "clothing"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # 상의, 하의, 아우터, 원피스
    image_url = Column(String(500), nullable=False)
    brand = Column(String(100))
    price = Column(Integer, default=0)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# models/try_on_request.py
class TryOnRequest(Base):
    __tablename__ = "try_on_request"

    id = Column(String(64), primary_key=True)
    clothing_id = Column(String(64), ForeignKey("clothing.id"), nullable=False)
    clothing_items = Column(JSON)
    face_image_path = Column(String(500), nullable=False)
    body_image_path = Column(String(500), nullable=False)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    result_image_url = Column(String(500))
    video_url = Column(String(500))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    clothing = relationship("Clothing", backref="try_on_requests")
```

### 6.4 데이터 모델 (TypeScript - Frontend)

```typescript
// types/clothing.ts
interface Clothing {
  id: string;
  name: string;
  category: "상의" | "하의" | "아우터" | "원피스";
  image_url: string;
  brand: string;
  price: number;
  description?: string;
}

// types/tryOnRequest.ts
interface TryOnRequest {
  id: string;
  clothing_id: string;
  clothing_items?: { id: string; category: "상의" | "하의" | "아우터" | "원피스" | "기타"; name?: string }[];
  face_image_path: string;
  body_image_path: string;
  status: "pending" | "processing" | "completed" | "failed";
  result_image_url?: string;
  video_url?: string;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}
```

---

## 7. 프로젝트 폴더 구조

```
fitter/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── frontend/                    # Next.js 프론트엔드
│   ├── package.json
│   ├── next.config.ts
│   ├── postcss.config.mjs
│   ├── public/
│   │   └── images/
│   │       ├── clothing/        # 의류 이미지
│   │       └── samples/         # 샘플 모델 사진
│   └── src/
│       ├── app/                 # Next.js App Router
│       │   ├── layout.tsx
│       │   ├── page.tsx         # 메인 페이지
│       │   ├── fitting/
│       │   │   └── page.tsx     # 피팅 서비스 페이지
│       │   └── result/
│       │       └── [id]/
│       │           └── page.tsx # 결과 페이지
│       ├── components/
│       │   ├── ui/
│       │   ├── layout/
│       │   ├── fitting/
│       │   └── common/
│       ├── lib/
│       │   └── api.ts
│       └── types/
│           ├── clothing.ts
│           └── tryOnRequest.ts
│
├── backend/                     # FastAPI 백엔드
│   ├── pyproject.toml           # Poetry 의존성
│   ├── alembic.ini
│   ├── alembic/                 # DB 마이그레이션
│   │   └── versions/
│   ├── app/
│   │   ├── main.py              # FastAPI 앱 진입점
│   │   ├── config.py            # 설정 관리
│   │   ├── database.py          # DB 연결
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── uploads/                 # 업로드된 이미지 (로컬 개발용)
│
├── data/                        # 샘플 데이터
│   ├── clothing.json            # 의류 시드 데이터
│   └── sample_images/
│
└── docs/                        # 문서
    └── PRD.md
```

※ `docs/API.md`, `docs/architecture.md` 등은 필요 시 추가 예정입니다.

---

## 8. 사용자 플로우

```
1. 메인 페이지 접속
   └─→ "AI 피팅룸" 버튼 클릭

2. 피팅 서비스 페이지
   ├─→ Step 0: 시작 화면 (모델 이미지 + START 버튼)
   ├─→ Step 1: 의상 선택
   ├─→ Step 2: 얼굴/전신 사진 업로드
   └─→ Step 3: "피팅하기" 버튼 클릭

3. 로딩/대기 화면
   └─→ 결과 생성 대기 (예상 시간 표시)

4. 결과 페이지
   ├─→ 합성 이미지 확인
   ├─→ "360도 보기" 버튼 클릭 (선택)
   │   └─→ 영상 로딩 → 영상 재생
   ├─→ 다운로드 버튼
   └─→ "다른 옷 입어보기" 버튼 → Step 3으로 이동
```

---

## 9. UI/UX 요구사항

### 9.1 메인 페이지
- 무신사 메인 페이지 스타일 유지
- 상단 헤더: 로고, 기본 메뉴 바 (비활성)
- 메인 배너 영역
- "AI 피팅룸" CTA 버튼: 눈에 띄는 위치, 강조 색상

### 9.2 피팅 서비스 페이지
- 스텝 진행 표시 (1/3, 2/3, 3/3)
- 드래그 앤 드롭 이미지 업로드
- 업로드된 이미지 미리보기
- 의상 그리드 뷰 (3-4열)

### 9.3 결과 페이지
- 대형 결과 이미지 중앙 배치
- Before/After 토글 또는 슬라이더
- 액션 버튼: 다운로드, 공유, 다시하기

### 9.4 로딩 상태
- 예상 대기 시간 표시
- 진행률 또는 스피너
- 취소 버튼

---

## 10. AI 프롬프트 설계

### 10.1 OpenAI GPT-Image 1.5 - Virtual Try-On 프롬프트

```
You are a professional fashion photographer. Generate a photo of the person
wearing the provided clothing item.

Requirements:
- Keep the person's face exactly as shown in the face reference image
- Use the body proportions from the full-body reference image
- Replace the clothing with the provided garment image
- Maintain a consistent pose: standing straight, front-facing, arms naturally at sides
- Use a clean, neutral background (white or light gray)
- Full body should be visible in the frame
- Professional studio lighting
- High quality, realistic result
- Resolution: 1024x1536

Reference images:
1. Face photo: [face_image]
2. Full body photo: [body_image]
3. Clothing item: [clothing_image]
```

### 10.2 Kling AI - 360도 회전 프롬프트

```
Create a smooth 360-degree rotation video of this person.
- Camera slowly rotates around the subject
- Subject remains stationary in the center
- Maintain consistent lighting throughout
- Duration: 5 seconds
- Smooth, professional motion
```

---

## 11. 개발 일정 (3일) - 병렬 개발 방식

### Day 1: 프로젝트 초기화 및 기본 구조

| 순서 | 작업 | 상세 내용 |
|------|------|----------|
| 1 | 프로젝트 초기화 | 모노레포 구조 생성, Git 초기화 |
| 2 | 프론트엔드 설정 | Next.js + TypeScript + Tailwind + Shadcn/ui |
| 3 | 백엔드 설정 | FastAPI + SQLAlchemy + Alembic |
| 4 | DB 설정 | PostgreSQL 컨테이너, 초기 마이그레이션 |
| 5 | 메인 페이지 UI | 무신사 스타일 메인 페이지 클론 |
| 6 | API 스켈레톤 | 엔드포인트 정의 (로직 미구현) |
| 7 | 의류 데이터 | 샘플 의류 이미지 준비, DB 시드 |

**Day 1 완료 기준:**
- [ ] 프론트엔드/백엔드 서버 각각 실행 가능
- [ ] 메인 페이지 UI 표시
- [ ] `/api/clothing` API가 샘플 데이터 반환
- [ ] PostgreSQL에 clothing 테이블 생성

### Day 2: 핵심 AI 기능 개발

| 순서 | 작업 | 상세 내용 |
|------|------|----------|
| 1 | OpenAI GPT-Image 연동 | API 키 설정, SDK 설치, 테스트 |
| 2 | 이미지 업로드 기능 | 프론트엔드 업로더 + 백엔드 핸들러 |
| 3 | Try-On 로직 구현 | 프롬프트 설계, 이미지 합성 파이프라인 |
| 4 | 프론트-백엔드 연동 | API 호출, 결과 표시 |
| 5 | 피팅 서비스 페이지 | Step 1~3 UI 완성 |
| 6 | 결과 페이지 | 합성 이미지 표시, 다운로드 |
| 7 | Kling AI 연동 | Image-to-Video API 테스트 |

**Day 2 완료 기준:**
- [ ] 사진 업로드 → AI 합성 → 결과 표시 전체 흐름 동작
- [ ] 최소 1개 의상으로 Try-On 성공
- [ ] Kling AI 영상 생성 테스트 완료

### Day 3: 통합, 개선 및 문서화

| 순서 | 작업 | 상세 내용 |
|------|------|----------|
| 1 | 버그 수정 | Day 2에서 발견된 이슈 해결 |
| 2 | 프롬프트 튜닝 | 합성 품질 개선, 포즈 일관성 |
| 3 | 360도 영상 통합 | Kling AI 영상을 결과 페이지에 연동 |
| 4 | UI 개선 | 로딩 상태, 에러 처리, 반응형 |
| 5 | 엣지 케이스 처리 | 잘못된 이미지, API 실패 등 |
| 6 | 테스트 | 다양한 입력으로 통합 테스트 |
| 7 | 문서화 | README, CLAUDE.md, 코드 정리 |
| 8 | 시연 준비 | 스크린샷, 데모 시나리오 |

**Day 3 완료 기준:**
- [ ] 전체 사용자 플로우 정상 동작
- [ ] 3개 이상 의상으로 Try-On 테스트 완료
- [ ] README.md 완성
- [ ] 시연 가능한 상태

---

## 12. 데이터 확보 전략

### 12.1 의류 데이터
- **소스**: HuggingFace, Kaggle 패션 데이터셋
- **필요 데이터**: 제품 이미지 (누끼/흰배경), 제품명
- **더미 데이터**: 가격, 브랜드명

### 12.2 추천 데이터셋
- [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
- [DeepFashion](http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html)

### 12.3 샘플 모델 사진
- 공개 라이선스 모델 사진 활용
- 또는 AI 생성 모델 이미지 사용

---

## 13. 리스크 및 대응 방안

| 리스크 | 영향 | 대응 방안 |
|--------|------|----------|
| GPT-Image API 품질 편차 | 높음 | 프롬프트 튜닝, 여러 번 시도 후 최적 결과 선택 |
| Kling AI API 접근 제한 | 중간 | 서드파티(Replicate, PiAPI) 활용 또는 사전 생성 영상 사용 |
| 3일 내 완성 불가 | 높음 | 영상 기능 우선순위 낮춤, 이미지 합성에 집중 |
| 합성 품질 저하 | 중간 | 후처리(얼굴 블렌딩, 해상도 업스케일) 적용 |
| API 비용 초과 | 낮음 | 무료 크레딧 활용, 테스트 횟수 제한 |

---

## 14. 성공 지표

### 14.1 기술적 지표
- [ ] 이미지 합성 성공률 > 80%
- [ ] 평균 이미지 생성 시간 < 30초
- [ ] 영상 생성 성공률 > 70%
- [ ] API 에러율 < 5%

### 14.2 데모 품질 지표
- [ ] 합성 이미지의 자연스러움 (주관적 평가)
- [ ] 얼굴 보존 정확도
- [ ] 의상 착용 사실감
- [ ] UI/UX 직관성

---

## 15. 향후 로드맵

### Phase 2 (데모 이후)
- 더 많은 의상 종류 지원
- 다양한 포즈 옵션
- 멀티뷰 입력 (정면 + 측면)

### Phase 3 (장기)
- 실시간 3D 렌더링
- 사이즈 추천 연동
- 실제 무신사 상품 DB 연동

---

## 16. 참고 자료

- [OpenAI Images API Docs](https://platform.openai.com/docs/api-reference/images)
- [Kling AI 개발자 문서](https://app.klingai.com/global/dev/document-api)
- [무신사 AI 포토부스 사례](https://blog.google/technology/ai/nano-banana-pro/)

---

*작성일: 2026-01-20*
*버전: 1.0*
