"""Local-only test for OpenAI image preprocessing."""
import io
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.openai_image import OpenAIImageService


def describe_image(label: str, data: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(data))
        width, height = image.size
        return f"{label}: {image.format} {width}x{height} ({len(data) / 1024:.1f} KB)"
    except UnidentifiedImageError:
        return f"{label}: unknown format ({len(data) / 1024:.1f} KB)"


def main() -> None:
    print("=" * 60)
    print("Testing local image preprocessing (no API call)")
    print("=" * 60)

    service = OpenAIImageService()
    print(f"Max side: {service.max_image_side}px")
    print(f"Max size: {service.max_image_bytes / (1024 * 1024):.1f} MB")
    print(f"JPEG quality: {service.jpeg_quality}")
    print(f"Force JPEG: {service.force_jpeg}")

    repo_root = Path(__file__).resolve().parents[2]

    def resolve_path(path: str) -> Path:
        if path.startswith("/"):
            relative_path = path.lstrip("/")
            candidates = [
                repo_root / "frontend" / "public" / relative_path,
                repo_root / "public" / relative_path,
            ]
            for candidate in candidates:
                if candidate.exists():
                    return candidate
        return Path(path)

    paths = [
        "/faceshot.jpeg",
        "/Fullshot.jpeg",
        "/Model_CUT.png",
    ]

    print("\nInputs:")
    for path in paths:
        resolved = resolve_path(path)
        if not resolved.exists():
            print(f"- Missing: {path}")
            continue

        raw_bytes = resolved.read_bytes()
        raw_mime = service._guess_mime_type(str(resolved))
        processed_bytes, processed_mime = service._process_image_bytes(raw_bytes, raw_mime)

        print(f"\n- {path} -> {resolved}")
        print(describe_image("  Original", raw_bytes))
        print(describe_image("  Processed", processed_bytes))
        print(f"  MIME: {raw_mime} -> {processed_mime}")
        print(
            f"  Size delta: {len(processed_bytes) - len(raw_bytes):,} bytes"
        )

    print("\nDone.")


if __name__ == "__main__":
    main()
