# TODO

## Recent Changes
- 루트 `/`는 `/musinsa`로 리다이렉트됨 (`frontend/src/app/(site)/page.tsx`).
- 무신사 헤더에 `/fitting` 이동 CTA 추가 (`frontend/src/components/musinsa/MusinsaHeader.tsx`).
- 피팅 이미지 프리뷰를 `next/image`로 전환 (`frontend/src/components/fitting/*`).
- Google Fonts `<link>` 로딩 및 폰트 변수 추가 (`frontend/src/app/layout.tsx`, `frontend/src/app/globals.css`).
- 프론트 빌드가 `next build --webpack` 사용 (`frontend/package.json`).

## Current Status
- 무신사 메인 페이지와 피팅 플로우 UI 구현됨 (라우팅: `/`→`/musinsa`, `/fitting`).
- 의상 목록/피팅 요청/결과 조회 API는 백엔드에서 제공됨.
- 데이터셋 확정 전이므로 스키마/API 변경 가능성이 있음.

## Scope / Non-scope (Today)
- Scope: 메인 라우팅/CTA 동작 확인, 피팅 플로우 UI 확인, 실패 케이스 UX 보강.
- Non-scope: 백엔드 스키마 수정, AI 모델 튜닝, 배포 작업.

## Risks / Unknowns
- `next dev`가 중복 실행되면 `.next/dev/lock` 에러 발생.
- `/api/clothing` 실패 시 무신사 페이지가 에러로 중단됨.
- `next/image`가 `unoptimized`로 동작 중이라 최적화 정책 재검토 필요.

## Next Tasks
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
