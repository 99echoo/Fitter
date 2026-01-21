"use client";

import Image from "next/image";
import { Clothing, ClothingCategory } from "@/types";

interface ClothingSelectorProps {
  items: Clothing[];
  onSelect: (clothings: Clothing[]) => void;
  selectedIds: string[];
}

const CATEGORIES: ClothingCategory[] = ["상의", "하의", "아우터"];

export function ClothingSelector({
  items,
  onSelect,
  selectedIds,
}: ClothingSelectorProps) {
  const groupedItems = CATEGORIES.map((category) => ({
    category,
    items: items.filter((item) => item.category === category),
  })).filter((group) => group.items.length > 0);

  const handleSelect = (item: Clothing) => {
    const currentSelected = items.filter((i) => selectedIds.includes(i.id));
    const isSelected = selectedIds.includes(item.id);

    if (isSelected) {
      onSelect(currentSelected.filter((i) => i.id !== item.id));
      return;
    }

    const withoutCategory = currentSelected.filter(
      (i) => i.category !== item.category
    );
    onSelect([...withoutCategory, item]);
  };

  return (
    <div className="space-y-5">
      {groupedItems.length === 0 && (
        <p className="text-center text-gray-500 py-8">
          상품이 없습니다.
        </p>
      )}

      {groupedItems.map((group) => (
        <section key={group.category}>
          <div className="flex gap-2 overflow-x-auto pb-2 snap-x snap-mandatory scrollbar-hide">
            {group.items.map((item) => (
              <div
                key={item.id}
                className={`shrink-0 w-33 cursor-pointer transition-all snap-start rounded overflow-hidden ${
                  selectedIds.includes(item.id)
                    ? "ring-2 ring-black"
                    : "hover:opacity-80"
                }`}
                onClick={() => handleSelect(item)}
              >
                <div className="aspect-[3/4] relative bg-neutral-100">
                  <Image
                    src={item.image_url}
                    alt={item.name}
                    fill
                    sizes="9rem"
                    className="object-cover"
                    unoptimized
                  />
                </div>
              </div>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
