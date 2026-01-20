export type MusinsaProduct = {
  id: string | number;
  rank: number;
  brand: string;
  name: string;
  price: string;
  salePrice?: string;
  discountRate?: string;
  badge?: string;
  likeCount?: string;
  colors?: string[];
  image: string;
};

const makeImage = (label: string, color: string) => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">
    <defs>
      <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="${color}" />
        <stop offset="100%" stop-color="#f5f5f5" />
      </linearGradient>
    </defs>
    <rect width="600" height="600" fill="url(#g)" />
    <text x="50%" y="50%" font-size="36" font-family="Arial, sans-serif" fill="#3f3f46" text-anchor="middle" dominant-baseline="middle">${label}</text>
  </svg>`;

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
};

export const musinsaProducts: MusinsaProduct[] = [
  {
    id: 1,
    rank: 1,
    brand: "아디다스",
    name: "라이트폼 러닝 슈즈",
    price: "109,000원",
    salePrice: "81,900원",
    discountRate: "25%",
    badge: "쿠폰",
    likeCount: "4.1만",
    colors: ["#111827", "#6b7280", "#9ca3af"],
    image: makeImage("SNEAKER", "#e5e7eb"),
  },
  {
    id: 2,
    rank: 2,
    brand: "뉴발란스",
    name: "530 클래식 스니커즈",
    price: "129,000원",
    salePrice: "109,000원",
    discountRate: "16%",
    likeCount: "2.6만",
    colors: ["#d1d5db", "#a1a1aa"],
    image: makeImage("RUNNER", "#e7e5e4"),
  },
  {
    id: 3,
    rank: 3,
    brand: "스투시",
    name: "오프화이트 스트라이프 롱 슬리브",
    price: "89,000원",
    salePrice: "69,000원",
    discountRate: "22%",
    badge: "할인",
    likeCount: "1.9만",
    colors: ["#0f172a", "#e2e8f0"],
    image: makeImage("TOP", "#f5f5f4"),
  },
  {
    id: 4,
    rank: 4,
    brand: "라코스테",
    name: "클래식 집업 니트",
    price: "189,000원",
    salePrice: "132,000원",
    discountRate: "30%",
    likeCount: "8,900",
    colors: ["#1f2937", "#e5e7eb"],
    image: makeImage("KNIT", "#e2e8f0"),
  },
  {
    id: 5,
    rank: 5,
    brand: "유니클로",
    name: "에어리즘 릴렉스 니트 - 5 COLOR",
    price: "39,000원",
    salePrice: "27,900원",
    discountRate: "28%",
    badge: "쿠폰",
    likeCount: "2.1만",
    colors: ["#111827", "#d1d5db", "#9ca3af", "#f97316", "#60a5fa"],
    image: makeImage("KNIT", "#f3f4f6"),
  },
  {
    id: 6,
    rank: 6,
    brand: "디스이즈네버댓",
    name: "패커블 덕다운 파카 - 3 COLOR",
    price: "229,000원",
    salePrice: "159,000원",
    discountRate: "31%",
    likeCount: "9,900",
    colors: ["#111827", "#9ca3af", "#e5e7eb"],
    image: makeImage("PUFFER", "#e5e7eb"),
  },
  {
    id: 7,
    rank: 7,
    brand: "에잇세컨즈",
    name: "코튼 케이블 가디건",
    price: "59,900원",
    salePrice: "39,900원",
    discountRate: "33%",
    likeCount: "7,200",
    colors: ["#f3f4f6", "#111827"],
    image: makeImage("CARDIGAN", "#ede9fe"),
  },
  {
    id: 8,
    rank: 8,
    brand: "무신사 스탠다드",
    name: "릴렉스 핏 스웨트셔츠",
    price: "29,900원",
    salePrice: "23,900원",
    discountRate: "20%",
    badge: "배송",
    likeCount: "1.2만",
    colors: ["#111827", "#475569", "#f97316"],
    image: makeImage("SWEAT", "#f1f5f9"),
  },
  {
    id: 9,
    rank: 9,
    brand: "나이키",
    name: "클럽 플리스 크루넥",
    price: "79,000원",
    salePrice: "63,000원",
    discountRate: "20%",
    likeCount: "2.4만",
    colors: ["#111827", "#f3f4f6"],
    image: makeImage("CREW", "#e2e8f0"),
  },
  {
    id: 10,
    rank: 10,
    brand: "폴로 랄프 로렌",
    name: "시그니처 옥스포드 셔츠",
    price: "139,000원",
    salePrice: "111,000원",
    discountRate: "20%",
    likeCount: "8,200",
    colors: ["#60a5fa", "#f8fafc"],
    image: makeImage("SHIRT", "#f8fafc"),
  },
  {
    id: 11,
    rank: 11,
    brand: "오프화이트",
    name: "그래픽 후디",
    price: "249,000원",
    salePrice: "199,000원",
    discountRate: "20%",
    likeCount: "6,400",
    colors: ["#0f172a"],
    image: makeImage("HOODIE", "#e5e7eb"),
  },
  {
    id: 12,
    rank: 12,
    brand: "컨버스",
    name: "척 70 하이",
    price: "89,000원",
    salePrice: "69,000원",
    discountRate: "22%",
    likeCount: "3.1만",
    colors: ["#111827", "#f8fafc"],
    image: makeImage("CHUCK", "#e5e7eb"),
  },
];
