#!/usr/bin/env python3
import csv
import re
import sys
import urllib.request
from pathlib import Path

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


def classify_category(*parts: str) -> str:
    text = " ".join(part for part in parts if part).lower()
    tokens = WORD_BOUNDARY.split(text)
    token_set = set(tokens)
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in token_set or keyword in text:
                return category
    return "기타"


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

            row["image_url"] = local_url
            row["category"] = classify_category(raw_category, name, description)
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
