import Image from "next/image";
import type { MusinsaProduct } from "@/data/musinsaProducts";

export function ProductCard({ product }: { product: MusinsaProduct }) {
  const hasDiscount = Boolean(product.salePrice && product.discountRate);
  const displayPrice = product.salePrice ?? product.price;

  return (
    <article className="group text-left">
      <div className="relative aspect-square w-full overflow-hidden rounded-sm bg-neutral-100">
        <Image
          src={product.image}
          alt={`${product.brand} ${product.name}`}
          fill
          sizes="(min-width: 1280px) 16vw, (min-width: 1024px) 24vw, (min-width: 640px) 33vw, 50vw"
          className="object-cover transition-transform duration-300 group-hover:scale-105"
          unoptimized
        />
        <span className="absolute left-2 top-2 rounded bg-white/90 px-1.5 py-0.5 text-[11px] font-semibold text-neutral-900">
          {product.rank}
        </span>
        <button
          type="button"
          className="absolute bottom-2 right-2 rounded-full border border-neutral-200 bg-white/90 p-1 text-neutral-500 transition hover:text-neutral-900"
          aria-label="찜하기"
        >
          <svg viewBox="0 0 24 24" className="h-4 w-4">
            <path
              d="M12 20s-6.5-4.2-8.5-7.7C1.6 9.3 3.2 6 6.4 6c1.8 0 3.1 1 3.6 2.1C10.5 7 11.8 6 13.6 6c3.2 0 4.8 3.3 2.9 6.3C18.5 15.8 12 20 12 20z"
              fill="currentColor"
            />
          </svg>
        </button>
      </div>

      <div className="mt-2 space-y-1">
        <div className="text-[11px] font-semibold text-neutral-800">
          {product.brand}
        </div>
        <div className="text-xs text-neutral-800 line-clamp-2">
          {product.name}
        </div>
        <div className="flex items-baseline gap-1 text-neutral-900">
          {hasDiscount && (
            <span className="text-[11px] font-semibold text-red-500">
              {product.discountRate}
            </span>
          )}
          <span className="text-sm font-semibold">{displayPrice}</span>
          {hasDiscount && (
            <span className="text-[11px] text-neutral-400 line-through">
              {product.price}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 text-[11px] text-neutral-500">
          {product.badge && (
            <span className="rounded bg-neutral-100 px-1.5 py-0.5 font-semibold uppercase tracking-wide">
              {product.badge}
            </span>
          )}
          {product.likeCount && <span>판매 {product.likeCount}</span>}
        </div>
        {product.colors && product.colors.length > 0 && (
          <div className="flex gap-1">
            {product.colors.map((color) => (
              <span
                key={color}
                className="h-2.5 w-2.5 rounded-full border border-neutral-200"
                style={{ backgroundColor: color }}
              />
            ))}
          </div>
        )}
      </div>
    </article>
  );
}
