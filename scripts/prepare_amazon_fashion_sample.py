#!/usr/bin/env python3
import csv
import hashlib
import random
import re
import sys
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

INPUT_CSV = Path("data/amazon_fashion_100k_sample_200.csv")
OUTPUT_CSV = Path("data/amazon_fashion_100k_sample_200_local.csv")
IMAGE_DIR = Path("frontend/public/amazon_fashion")

KEYWORDS = {
    "원피스": [
        "dress",
        "jumpsuit",
        "romper",
    ],
    "아우터": [
        "coat",
        "jacket",
        "parka",
        "outerwear",
        "blazer",
        "windbreaker",
        "puffer",
        "down",
        "trench",
        "vest",
    ],
    "하의": [
        "pants",
        "jeans",
        "shorts",
        "skirt",
        "trousers",
        "leggings",
        "jogger",
        "sweatpants",
        "slacks",
    ],
    "상의": [
        "top",
        "t-shirt",
        "tee",
        "shirt",
        "blouse",
        "sweater",
        "hoodie",
        "sweatshirt",
        "cardigan",
        "bra",
        "tank",
        "camisole",
        "tunic",
        "polo",
        "jersey",
        "knit",
    ],
}

WORD_BOUNDARY = re.compile(r"[\\W_]+")
MAIN_CATEGORY_RE = re.compile(r"Main Category:\\s*([^\\n\\r]+)", re.IGNORECASE)
SUB_CATEGORY_RE = re.compile(r"Sub Category:\\s*([^\\n\\r]+)", re.IGNORECASE)

CATEGORY_MAP = {
    # one-piece / sets
    "dress": "원피스",
    "romper": "원피스",
    "jumpsuit": "원피스",
    "outfit": "원피스",
    "outfit set": "원피스",
    "kurta set": "원피스",
    "legging pant set": "원피스",
    "pajamas": "원피스",
    "swimwear": "원피스",
    "robe": "원피스",
    "suit": "원피스",
    # bottoms
    "pants": "하의",
    "shorts": "하의",
    "skirt": "하의",
    "leggings": "하의",
    # tops
    "shirt": "상의",
    "t shirt": "상의",
    "tshirt": "상의",
    "top": "상의",
    "blouse": "상의",
    "hoodie": "상의",
    "jersey": "상의",
    "tank top": "상의",
    "athletic tank top": "상의",
    "bra": "상의",
    "bras": "상의",
    # outerwear
    "jacket": "아우터",
    "coat": "아우터",
    "poncho": "아우터",
    "vest": "아우터",
    "lab coat": "아우터",
    # accessories / other
    "footwear": "기타",
    "boot": "기타",
    "boots": "기타",
    "bootie": "기타",
    "sneaker": "기타",
    "sandals": "기타",
    "cleats": "기타",
    "bag": "기타",
    "handbag": "기타",
    "tote bag": "기타",
    "backpack": "기타",
    "hat": "기타",
    "cap": "기타",
    "headwear": "기타",
    "headband": "기타",
    "sunglasses": "기타",
    "glasses": "기타",
    "face cover": "기타",
    "mask": "기타",
    "neck gaiter": "기타",
    "socks": "기타",
    "gloves": "기타",
    "belt": "기타",
    "keychain": "기타",
    "pin": "기타",
    "anklet": "기타",
    "jewelry": "기타",
    "earrings": "기타",
    "necklace": "기타",
    "bracelet": "기타",
    "ring": "기타",
    "pendant": "기타",
    "brooch": "기타",
    "ring accessories": "기타",
    "watch": "기타",
    "watch box": "기타",
    "cord lock": "기타",
    "plant": "기타",
    "costume": "기타",
    "underwear": "기타",
    "lingerie": "기타",
    "bra pads": "기타",
    "hair accessories": "기타",
}

PRICE_RANGES = {
    "dress": (30, 160),
    "romper": (25, 120),
    "jumpsuit": (35, 160),
    "outfit": (35, 180),
    "outfit set": (35, 180),
    "kurta set": (35, 160),
    "legging pant set": (35, 160),
    "pajamas": (20, 80),
    "swimwear": (20, 110),
    "robe": (25, 90),
    "suit": (80, 350),
    "pants": (25, 120),
    "shorts": (15, 70),
    "skirt": (20, 90),
    "leggings": (18, 70),
    "shirt": (18, 80),
    "t shirt": (12, 50),
    "tshirt": (12, 50),
    "top": (15, 65),
    "blouse": (20, 90),
    "hoodie": (30, 90),
    "jersey": (25, 90),
    "tank top": (12, 45),
    "athletic tank top": (15, 55),
    "bra": (15, 60),
    "bras": (15, 60),
    "jacket": (40, 200),
    "coat": (50, 250),
    "poncho": (25, 80),
    "vest": (20, 90),
    "lab coat": (25, 90),
    "footwear": (30, 180),
    "boot": (50, 220),
    "boots": (50, 220),
    "bootie": (40, 180),
    "sneaker": (40, 160),
    "sandals": (20, 120),
    "cleats": (40, 160),
    "bag": (25, 180),
    "handbag": (30, 200),
    "tote bag": (20, 120),
    "backpack": (25, 160),
    "earrings": (10, 80),
    "necklace": (15, 120),
    "bracelet": (10, 70),
    "ring": (10, 80),
    "pendant": (15, 90),
    "brooch": (10, 60),
    "anklet": (8, 40),
    "jewelry": (12, 120),
    "watch": (50, 400),
    "watch box": (15, 80),
    "sunglasses": (15, 120),
    "glasses": (15, 120),
    "hat": (12, 50),
    "cap": (12, 45),
    "headwear": (10, 50),
    "headband": (8, 35),
    "belt": (10, 50),
    "socks": (6, 20),
    "gloves": (10, 45),
    "keychain": (5, 20),
    "pin": (5, 20),
    "cord lock": (3, 15),
    "mask": (5, 20),
    "face cover": (5, 20),
    "neck gaiter": (6, 25),
    "hair accessories": (5, 25),
    "bra pads": (5, 20),
    "ring accessories": (4, 20),
    "plant": (10, 40),
    "costume": (20, 80),
    "underwear": (10, 40),
    "lingerie": (15, 70),
}

CATEGORY_PRICE_RANGES = {
    "상의": (15, 80),
    "하의": (20, 110),
    "아우터": (40, 200),
    "원피스": (30, 170),
    "기타": (10, 80),
}


def normalize_label(text: str) -> str:
    return WORD_BOUNDARY.sub(" ", text).strip().lower()


def extract_main_sub(description: str) -> Tuple[Optional[str], Optional[str]]:
    if not description:
        return None, None
    main_match = MAIN_CATEGORY_RE.search(description)
    sub_match = SUB_CATEGORY_RE.search(description)
    main = main_match.group(1).strip() if main_match else None
    sub = sub_match.group(1).strip() if sub_match else None
    return main, sub


def classify_by_keywords(*parts: str) -> str:
    text = " ".join(part for part in parts if part).lower()
    tokens = WORD_BOUNDARY.split(text)
    token_set = set(tokens)
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in token_set or keyword in text:
                return category
    return "기타"


def classify_category(raw_category: str, name: str, description: str) -> str:
    main, sub = extract_main_sub(description)
    for candidate in (main, sub, raw_category):
        if candidate:
            mapped = CATEGORY_MAP.get(normalize_label(candidate))
            if mapped:
                return mapped
    return classify_by_keywords(raw_category, name, description)


def parse_price(raw: str) -> Optional[float]:
    if raw is None:
        return None
    value = str(raw).strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def generate_price(parent_asin: str, main: Optional[str], category: str) -> str:
    seed = int(hashlib.md5(parent_asin.encode("utf-8")).hexdigest(), 16)
    rng = random.Random(seed)
    main_key = normalize_label(main) if main else None
    min_price, max_price = PRICE_RANGES.get(main_key, CATEGORY_PRICE_RANGES[category])
    price = rng.uniform(min_price, max_price)
    price = round(price + 1e-9, 2)
    return f"{price:.2f}"


def download_image(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    if not url:
        return False
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            dest.write_bytes(resp.read())
        return True
    except Exception:
        return False


def main() -> int:
    if not INPUT_CSV.exists():
        print(f"Missing input file: {INPUT_CSV}", file=sys.stderr)
        return 1

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    downloaded = 0
    failed = 0

    with INPUT_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parent_asin = row.get("parent_asin", "").strip()
            image_url = row.get("image_url", "").strip()
            if not parent_asin:
                continue

            ext = Path(image_url.split("?")[0]).suffix or ".jpg"
            filename = f"{parent_asin}{ext}"
            dest_path = IMAGE_DIR / filename
            ok = download_image(image_url, dest_path)
            if ok:
                downloaded += 1
                local_url = f"/amazon_fashion/{filename}"
            else:
                failed += 1
                local_url = image_url

            name = row.get("name", "").strip()
            description = row.get("description", "").strip()
            raw_category = row.get("category", "").strip()
            main, _sub = extract_main_sub(description)

            row["image_url"] = local_url
            row["category"] = classify_category(raw_category, name, description)
            if row["category"] not in CATEGORY_PRICE_RANGES:
                row["category"] = "기타"
            if parse_price(row.get("price")) is None:
                row["price"] = generate_price(parent_asin, main, row["category"])
            rows.append(row)

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "parent_asin",
                "name",
                "description",
                "image_url",
                "brand",
                "price",
                "category",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Downloaded: {downloaded}, Failed: {failed}")
    print(f"Wrote: {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
