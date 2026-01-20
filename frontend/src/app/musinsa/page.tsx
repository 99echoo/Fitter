import { MusinsaHeader } from "@/components/musinsa/MusinsaHeader";
import { AnnouncementBar } from "@/components/musinsa/AnnouncementBar";
import { RankingFilters } from "@/components/musinsa/RankingFilters";
import { ProductGrid } from "@/components/musinsa/ProductGrid";
import type { MusinsaProduct } from "@/data/musinsaProducts";
import type { ClothingListResponse } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const PRICE_FORMATTER = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const formatPrice = (price: number | null | undefined) => {
  if (typeof price !== "number" || price <= 0) {
    return "가격 정보 없음";
  }
  return PRICE_FORMATTER.format(price);
};

export default async function MusinsaPage() {
  const response = await fetch(`${API_BASE_URL}/api/clothing`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("의상 데이터를 불러오는데 실패했습니다.");
  }
  const data = (await response.json()) as ClothingListResponse;
  const products: MusinsaProduct[] = (data.items ?? []).map((item, index) => ({
    id: item.id,
    rank: index + 1,
    brand: item.brand || "브랜드 미상",
    name: item.name,
    price: formatPrice(item.price),
    image: item.image_url,
  }));

  return (
    <div className="min-h-screen bg-white text-neutral-900">
      <MusinsaHeader />
      <main className="mx-auto w-full max-w-[1300px] px-4 pb-16">
        <AnnouncementBar />
        <RankingFilters />
        <div className="mt-4 flex items-center justify-between text-xs text-neutral-500">
          <span>총 {products.length}개 상품</span>
          <div className="flex items-center gap-3">
            <button type="button">인기순</button>
            <button type="button">신상품</button>
            <button type="button">가격높은순</button>
            <button type="button">가격낮은순</button>
          </div>
        </div>
        <ProductGrid products={products} />
      </main>
    </div>
  );
}
