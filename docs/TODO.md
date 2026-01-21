# TODO

## Recent Changes
- 루트 `/`는 `/musinsa`로 리다이렉트됨 (`frontend/src/app/(site)/page.tsx`).
- 무신사 플로팅 CTA로 `/fitting` 이동 제공 (`frontend/src/components/musinsa/FittingFloatingCTA.tsx`).
- 피팅 이미지 프리뷰를 `next/image`로 전환 (`frontend/src/components/fitting/*`).
- 피팅 플로우를 시작 화면 → 의상 선택 → 사진 업로드로 재구성 (`frontend/src/app/(site)/fitting/page.tsx`).
- 의상 선택 UI를 카테고리별 가로 스크롤로 변경 (`frontend/src/components/fitting/ClothingSelector.tsx`).
- Google Fonts `<link>` 로딩 및 폰트 변수 추가 (`frontend/src/app/layout.tsx`, `frontend/src/app/globals.css`).
- 프론트 빌드가 `next build --webpack` 사용 (`frontend/package.json`).
- OpenAI GPT-Image 서비스에 이미지 경로/URL 해석 및 응답 검증 로직 보강 (`backend/app/services/openai_image.py`).
- GPT-Image 기본 모델을 `gpt-image-1.5`로 설정하고 환경변수로 분리 (`backend/app/config.py`, `backend/app/services/openai_image.py`).
- `/api/try-on` 입력을 `clothing_ids` 배열로 정리하고 카테고리 중복을 차단 (`backend/app/routers/try_on.py`).
- 결과 이미지/영상 상대 URL을 프론트에서 베이스 URL로 해석하도록 유틸 추가 (`frontend/src/lib/url.ts`, `frontend/src/app/(site)/result/[id]/page.tsx`).
- try_on_request에 `clothing_items` JSON 컬럼 추가 (alembic migration).
- OpenAI 이미지 출력 기본 사이즈를 1024x1536으로 변경 (`backend/app/config.py`, `docs/API_SETUP.md`).

## Current Status
- 무신사 메인 페이지와 피팅 플로우 UI 구현됨 (라우팅: `/`→`/musinsa`, `/fitting`).
- 피팅 플로우: 시작 화면 → 의상 선택 → 얼굴/전신 사진 업로드 → 대기 → 결과.
- 의상 목록/피팅 요청/결과 조회 API는 백엔드에서 제공됨.
- try-on 결과는 `/uploads/results/...`로 저장되며 결과 API는 상대 경로를 반환함.
- AI 연동 서비스(OpenAI GPT-Image/Kling) 코드가 있으나 실제 API 키 연동/결과 저장 검증은 추가 확인 필요.
- 데이터셋 확정 전이므로 스키마/API 변경 가능성이 있음.

## Scope / Non-scope (Today)
- Scope: AI 모델 연동 계획 수립, try-on/video API 흐름 점검, 업로드/결과 URL 규칙 정리.
- Non-scope: 백엔드 스키마 대규모 변경, UI 리디자인, 배포 작업.

## Risks / Unknowns
- `next dev`가 중복 실행되면 `.next/dev/lock` 에러 발생.
- OpenAI GPT-Image/Kling API 요청 스펙과 응답 포맷이 실제로 검증되지 않음.
- 로컬 파일 경로(`/uploads`)와 원격 URL 처리 방식이 혼재됨.
- 결과 페이지에서 이미지가 표시되지 않는 케이스가 보고됨 (베이스 URL/캐시/재시작 여부 확인 필요).
- `.env`에 실제 키가 포함되어 있을 가능성 있음 (비밀정보 회수/샘플 분리 필요).

## Next Tasks
- [TASK-104] 결과 페이지 이미지 표시 이슈 재현/해결
  - 목표: `/result/:id`에서 이미지가 안정적으로 표시되도록 원인 확정 및 수정
  - 대상: `frontend/src/app/(site)/result/[id]/page.tsx`, `frontend/src/lib/url.ts`, `backend/app/main.py`
  - 작업:
    - [ ] 브라우저 Network에서 실제 이미지 요청 URL/응답 확인
    - [ ] `NEXT_PUBLIC_API_URL` 설정/재시작 여부 확인
    - [ ] `/uploads` 정적 서빙 경로 확인 및 문서화
  - 완료 조건(DoD):
    - 결과 페이지에서 이미지가 항상 표시됨
  - 테스트 힌트:
    - `http://localhost:8000/uploads/...` 직접 접근

- [TASK-105] 비밀정보 정리
  - 목표: 실제 키/토큰이 리포지토리에 남지 않도록 정리
  - 대상: `.env`, `.env.example`, `docs/API_SETUP.md`
  - 작업:
    - [ ] 실 키/토큰 제거 후 샘플 값으로 대체
    - [ ] 키 재발급/회수 여부 확인
  - 완료 조건(DoD):
    - 리포지토리에 민감정보 없음
  - 테스트 힌트:
    - `rg -n \"API_KEY|SECRET|TOKEN\" -S .`
- [TASK-101] OpenAI GPT-Image 연동 검증 및 이미지 파이프라인 정리
  - 목표: try-on 요청이 실제 API 호출로 이미지 생성되고 결과 URL이 접근 가능하도록 정리
  - 대상: `backend/app/services/openai_image.py`, `backend/app/routers/try_on.py`, `backend/app/utils/file_handler.py`, `backend/app/config.py`
  - 작업:
    - [ ] OpenAI Images API 요청/응답 형식 확인 및 에러 처리 보강
    - [ ] 로컬 파일/원격 URL 경로 처리 일관화(`/uploads` 포함)
    - [ ] 실패 시 status/error_message 업데이트 및 재시도 정책 결정
  - 완료 조건(DoD):
    - try-on 1건 성공, `result_image_url`로 이미지 접근 확인
  - 테스트 힌트:
    - `cd backend && poetry run uvicorn app.main:app --reload`

- [TASK-102] Kling AI 영상 생성 연동 검증 및 폴링 정리
  - 목표: 생성된 이미지로 영상 생성이 성공하고 결과 페이지에서 재생 가능하도록 보강
  - 대상: `backend/app/services/kling_ai.py`, `backend/app/routers/video.py`, `frontend/src/app/(site)/result/[id]/page.tsx`, `frontend/src/components/fitting/ResultViewer.tsx`
  - 작업:
    - [ ] Kling API 요청 스펙 확인(모델 ID, base64/URL 방식)
    - [ ] 폴링 종료 조건 및 실패 처리 정리
    - [ ] `video_url` 저장 후 프론트 재생 확인
  - 완료 조건(DoD):
    - `/api/generate-video` 호출 후 결과 페이지에서 영상 재생 가능
  - 테스트 힌트:
    - `/result/:id`에서 영상 생성 버튼 클릭

- [TASK-103] AI 연동 환경/스토리지/URL 규칙 정리
  - 목표: API 키/업로드 경로/결과 URL 규칙을 문서와 코드에서 일관되게 유지
  - 대상: `.env.example`, `backend/app/config.py`, `backend/app/main.py`, `frontend/src/lib/api.ts`
  - 작업:
    - [ ] `.env` 키/설명 및 기본값 점검
    - [ ] 업로드/결과 URL 생성 규칙 문서화(상대/절대 처리)
    - [ ] 프론트에서 상대 URL 처리 기준 정리
  - 완료 조건(DoD):
    - 로컬에서 업로드/결과 URL 접근 가능, 규칙이 문서에 반영됨
  - 테스트 힌트:
    - 업로드 후 `/uploads/...` 직접 접근

- [TASK-001] 메인 라우팅 & CTA 확인
  - 목표: `/` 진입 시 `/musinsa` 노출, CTA 클릭 시 `/fitting` 이동
  - 대상: `frontend/src/app/(site)/page.tsx`, `frontend/src/components/musinsa/MusinsaHeader.tsx`
  - 작업:
    - [ ] dev 서버 1개만 실행 후 `/` 접근
    - [ ] CTA 버튼 클릭으로 `/fitting` 이동 확인
  - 완료 조건(DoD):
    - `/`에서 무신사 메인 렌더, CTA로 피팅 진입 정상
  - 테스트 힌트:
    - `cd frontend && npm run dev`

- [TASK-002] 피팅 플로우 데이터 로딩 확인
  - 목표: 의상 목록 로드 및 피팅 요청 플로우 확인
  - 대상: `frontend/src/app/(site)/fitting/page.tsx`, `frontend/src/components/fitting/*`
  - 작업:
    - [ ] 의상 리스트 로딩 확인
    - [ ] 이미지 업로드 및 요청 시 에러 메시지 확인
  - 완료 조건(DoD):
    - 의상 리스트/업로드/요청 단계가 막힘 없이 진행
  - 테스트 힌트:
    - `/fitting`에서 샘플 이미지 업로드 테스트

- [TASK-003] 무신사 페이지 API 실패 UX 보강
  - 목표: `/api/clothing` 실패 시 사용자 안내 제공
  - 대상: `frontend/src/app/musinsa/page.tsx`
  - 작업:
    - [ ] fetch 실패 시 fallback UI 또는 에러 메시지 추가
  - 완료 조건(DoD):
    - 백엔드 미기동 시에도 안내 UI 표시
  - 테스트 힌트:
    - 백엔드 중지 후 `/musinsa` 진입
