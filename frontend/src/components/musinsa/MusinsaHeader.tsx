const topNavItems = [
  "MUSINSA",
  "BEAUTY",
  "PLAYER",
  "OUTLET",
  "BOUTIQUE",
  "SHOES",
  "KIDS",
  "USED",
  "SNAP",
];

const sectionTabs = [
  "컨텐츠",
  "추천",
  "랭킹",
  "세일",
  "회원 쿠폰",
  "클리어런스 특가",
  "발매",
];

export function MusinsaHeader() {
  return (
    <header className="bg-neutral-900 text-neutral-100">
      <div className="border-b border-neutral-800">
        <div className="mx-auto flex w-full max-w-[1300px] items-center justify-between px-4 py-2 text-[11px]">
          <div className="flex items-center gap-4">
            <button
              type="button"
              className="flex items-center justify-center"
              aria-label="메뉴 열기"
            >
              <svg viewBox="0 0 24 24" className="h-4 w-4">
                <path
                  d="M4 6h16M4 12h16M4 18h16"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                />
              </svg>
            </button>
            <span className="text-sm font-semibold tracking-wide">MUSINSA</span>
            <nav className="hidden items-center gap-3 lg:flex">
              {topNavItems.slice(1).map((item) => (
                <span key={item} className="text-neutral-300">
                  {item}
                </span>
              ))}
            </nav>
          </div>
          <div className="flex items-center gap-3 text-neutral-300">
            <span className="hidden sm:inline">오프라인 스토어</span>
            <button type="button" className="flex items-center gap-1">
              <span className="hidden md:inline">검색</span>
              <svg viewBox="0 0 24 24" className="h-4 w-4">
                <circle
                  cx="11"
                  cy="11"
                  r="6"
                  stroke="currentColor"
                  strokeWidth="1.5"
                />
                <path
                  d="M20 20l-3.5-3.5"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                />
              </svg>
            </button>
            <button type="button" className="hidden sm:flex items-center gap-1">
              좋아요
            </button>
            <button type="button" className="hidden sm:flex items-center gap-1">
              마이
            </button>
            <button type="button" className="hidden sm:flex items-center gap-1">
              장바구니
            </button>
            <button
              type="button"
              className="rounded-full border border-neutral-700 px-3 py-1 text-[10px]"
            >
              로그인 / 회원가입
            </button>
          </div>
        </div>
      </div>

      <div className="border-b border-neutral-800">
        <div className="mx-auto flex w-full max-w-[1300px] flex-col gap-3 px-4 py-4 lg:flex-row lg:items-center">
          <div className="text-xl font-semibold tracking-tight">MUSINSA</div>
          <div className="relative flex-1">
            <input
              type="search"
              placeholder="브랜드, 상품, 할인정보를 검색해보세요"
              className="h-11 w-full rounded-md border border-neutral-200 bg-white px-4 text-sm text-neutral-900 placeholder:text-neutral-400"
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400">
              <svg viewBox="0 0 24 24" className="h-5 w-5">
                <circle
                  cx="11"
                  cy="11"
                  r="6"
                  stroke="currentColor"
                  strokeWidth="1.5"
                />
                <path
                  d="M20 20l-3.5-3.5"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                />
              </svg>
            </span>
          </div>
          <div className="hidden items-center gap-4 text-xs text-neutral-300 lg:flex">
            <span>오프라인 스토어</span>
            <span>고객센터</span>
            <span>매거진</span>
          </div>
        </div>

        <div className="mx-auto flex w-full max-w-[1300px] items-center gap-4 px-4 pb-3 text-sm">
          {sectionTabs.map((tab) => (
            <button
              key={tab}
              type="button"
              className={`pb-2 text-neutral-400 transition ${
                tab === "랭킹"
                  ? "border-b-2 border-white text-white"
                  : "hover:text-white"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
