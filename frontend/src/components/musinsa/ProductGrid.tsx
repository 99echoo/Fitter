import type { MusinsaProduct } from "@/data/musinsaProducts";
import { ProductCard } from "@/components/musinsa/ProductCard";

export function ProductGrid({ products }: { products: MusinsaProduct[] }) {
  return (
    <section className="mt-6">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </section>
  );
}
