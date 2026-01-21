"use client";

import { useState } from "react";
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
  const [activeCategory, setActiveCategory] = useState<ClothingCategory | "전체">("전체");

  const filteredItems =
    activeCategory === "전체"
      ? items
      : items.filter((item) => item.category === activeCategory);

  return (
    <div className="space-y-4">
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setActiveCategory("전체")}
          className={`px-4 py-2 rounded-full text-sm transition-colors ${
            activeCategory === "전체"
              ? "bg-primary text-primary-foreground"
              : "bg-muted hover:bg-muted/80"
          }`}
        >
          전체
        </button>
        {CATEGORIES.map((category) => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            className={`px-4 py-2 rounded-full text-sm transition-colors ${
              activeCategory === category
                ? "bg-primary text-primary-foreground"
                : "bg-muted hover:bg-muted/80"
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredItems.map((item) => (
          <Card
            key={item.id}
            className={`cursor-pointer transition-all hover:shadow-md ${
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
                  sizes="(min-width: 1024px) 25vw, (min-width: 768px) 33vw, 50vw"
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

      {filteredItems.length === 0 && (
        <p className="text-center text-muted-foreground py-8">
          해당 카테고리에 상품이 없습니다.
        </p>
      )}
    </div>
  );
}
