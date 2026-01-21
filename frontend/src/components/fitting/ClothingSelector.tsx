"use client";

import Image from "next/image";
import { Card, CardContent } from "@/components/ui/card";
import { Clothing, ClothingCategory } from "@/types";

interface ClothingSelectorProps {
  items: Clothing[];
  onSelect: (clothing: Clothing) => void;
  selectedId?: string;
}

const CATEGORIES: ClothingCategory[] = ["상의", "하의", "아우터", "원피스", "기타"];
const PRICE_FORMATTER = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

export function ClothingSelector({
  items,
  onSelect,
  selectedId,
}: ClothingSelectorProps) {
  const groupedItems = CATEGORIES.map((category) => ({
    category,
    items: items.filter((item) => item.category === category),
  })).filter((group) => group.items.length > 0);

  return (
    <div className="space-y-6">
      {groupedItems.length === 0 && (
        <p className="text-center text-muted-foreground py-8">
          해당 카테고리에 상품이 없습니다.
        </p>
      )}

      {groupedItems.map((group) => (
        <section key={group.category} className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">{group.category}</h3>
            <span className="text-xs text-muted-foreground">
              {group.items.length}개
            </span>
          </div>
          <div className="flex gap-3 overflow-x-auto pb-2 snap-x snap-mandatory">
            {group.items.map((item) => (
              <Card
                key={item.id}
                className={`shrink-0 w-40 sm:w-44 md:w-48 cursor-pointer transition-all hover:shadow-md snap-start ${
                  selectedId === item.id
                    ? "ring-2 ring-primary"
                    : ""
                }`}
                onClick={() => onSelect(item)}
              >
                <CardContent className="p-3">
                  <div className="aspect-square relative mb-2 bg-muted rounded-lg overflow-hidden">
                    <Image
                      src={item.image_url}
                      alt={item.name}
                      fill
                      sizes="(min-width: 1024px) 12rem, (min-width: 768px) 11rem, 10rem"
                      className="object-cover"
                      unoptimized
                    />
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">{item.brand}</p>
                    <p className="text-sm font-medium line-clamp-2">{item.name}</p>
                    <p className="text-sm font-bold">
                      {typeof item.price === "number" && item.price > 0
                        ? PRICE_FORMATTER.format(item.price)
                        : "가격 정보 없음"}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
