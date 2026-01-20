export type ClothingCategory = "상의" | "하의" | "아우터" | "원피스" | "기타";

export interface Clothing {
  id: string;
  name: string;
  category: ClothingCategory;
  image_url: string;
  brand: string;
  price?: number | null;
  description?: string;
}

export interface ClothingListResponse {
  items: Clothing[];
}
