const filterTabs = ["상품", "브랜드", "검색어"];

const categoryChips = [
  "NEW",
  "전체",
  "상의",
  "아우터",
  "니트",
  "팬츠",
  "가방",
  "슈즈",
  "스포츠/레저",
  "디지털/리빙",
  "키즈",
];

const subCategories = [
  "전체",
  "후디/스웨트",
  "맨투맨",
  "니트/스웨터",
  "셔츠",
  "반팔티",
  "긴팔티",
  "후드집업",
  "기타 상의",
];

export function RankingFilters() {
  return (
    <section className="mt-6 space-y-4 border-b border-neutral-200 pb-5">
      <div className="flex items-center gap-4 border-b border-neutral-200 pb-3 text-sm">
        {filterTabs.map((tab) => (
          <button
            key={tab}
            type="button"
            className={`pb-2 font-medium ${
              tab === "상품"
                ? "border-b-2 border-neutral-900 text-neutral-900"
                : "text-neutral-500 hover:text-neutral-900"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap gap-2 text-[11px] text-neutral-600">
        {categoryChips.map((chip) => (
          <button
            key={chip}
            type="button"
            className={`rounded-full border px-3 py-1 ${
              chip === "전체" || chip === "NEW"
                ? "border-neutral-900 text-neutral-900"
                : "border-neutral-200 hover:border-neutral-400"
            }`}
          >
            {chip}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-neutral-600">
        <div className="flex flex-wrap gap-3">
          {subCategories.map((category) => (
            <button
              key={category}
              type="button"
              className={`${
                category === "전체"
                  ? "font-semibold text-neutral-900"
                  : "hover:text-neutral-900"
              }`}
            >
              {category}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 text-neutral-500">
          <button type="button" className="font-semibold text-neutral-900">
            전체 랭킹
          </button>
          <span className="h-3 w-px bg-neutral-300" />
          <button type="button">실시간</button>
          <button type="button">주간</button>
          <button type="button">월간</button>
        </div>
      </div>
    </section>
  );
}
