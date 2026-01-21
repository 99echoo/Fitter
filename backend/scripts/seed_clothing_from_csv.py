#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
from typing import Optional

from sqlalchemy import delete

from app.database import SessionLocal
from app.models import Clothing, TryOnRequest

CATEGORIES = {"상의", "하의", "아우터", "원피스", "기타"}


def parse_price(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    value = str(raw).strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed clothing data from CSV.")
    parser.add_argument(
        "--csv",
        default="data/amazon_fashion_100k_sample_200_local.csv",
        help="Path to CSV file.",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Delete existing clothing rows before inserting.",
    )
    parser.add_argument(
        "--image-base-url",
        default="",
        help="Prefix for relative image URLs (e.g. http://localhost:3000).",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"Missing CSV: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    base_url = args.image_base_url.rstrip("/")
    session = SessionLocal()
    try:
        if args.truncate:
            session.execute(delete(TryOnRequest))
            session.execute(delete(Clothing))

        for row in rows:
            category = row.get("category", "").strip()
            if category not in CATEGORIES:
                category = "기타"

            image_url = row.get("image_url", "").strip()
            if base_url and image_url.startswith("/"):
                image_url = f"{base_url}{image_url}"

            item = Clothing(
                name=row.get("name", "").strip(),
                category=category,
                image_url=image_url,
                brand=row.get("brand", "").strip() or None,
                price=parse_price(row.get("price")),
                description=row.get("description", "").strip() or None,
            )
            session.add(item)

        session.commit()
    finally:
        session.close()

    print(f"Inserted {len(rows)} items from {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
