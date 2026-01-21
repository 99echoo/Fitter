"""Quick test for OpenAI GPT-Image API."""
import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.openai_image import OpenAIImageService, ClothingReference


async def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    print("=" * 60)
    print("Testing OpenAI GPT-Image API")
    print("=" * 60)
    print()

    # Initialize service
    try:
        service = OpenAIImageService()
        print("✓ OpenAIImageService initialized successfully")
        print(f"  Model: {service.model}")
    except Exception as e:
        print(f"✗ Failed to initialize service: {e}")
        return

    repo_root = Path(__file__).resolve().parents[2]

    def path_exists(path: str) -> bool:
        if path.startswith("/"):
            relative_path = path.lstrip("/")
            candidates = [
                repo_root / "frontend" / "public" / relative_path,
                repo_root / "public" / relative_path,
            ]
            return any(candidate.exists() for candidate in candidates)
        return Path(path).exists()

    def pick_existing_path(paths: list[str]) -> str:
        for candidate in paths:
            if path_exists(candidate):
                return candidate
        return paths[-1]

    # Prefer public assets, fall back to fixtures.
    face_candidates = ["/faceshot.jpeg", "tests/fixtures/sample_face.jpg"]
    body_candidates = ["/Fullshot.jpeg", "tests/fixtures/sample_body.jpg"]
    clothing_candidates = ["/Model_CUT.png", "tests/fixtures/sample_clothing.jpg"]

    face_path = pick_existing_path(face_candidates)
    body_path = pick_existing_path(body_candidates)
    clothing_path = pick_existing_path(clothing_candidates)

    if not path_exists(face_path) or not path_exists(body_path) or not path_exists(clothing_path):
        print("\n⚠  Missing test images.")
        print("   Add files to tests/fixtures/ or /public to run the full test.")
        return

    print("\nTest inputs:")
    print(f"  Face: {face_path}")
    print(f"  Body: {body_path}")
    print(f"  Clothing: {clothing_path}")

    try:
        print("\n🚀 Generating virtual try-on image...")
        print("   (This may take 10-30 seconds)")

        result_path = await service.generate_try_on(
            face_path,
            body_path,
            [ClothingReference(path=clothing_path, category="Top")],
        )

        print(f"\n✓ Success! Result saved to: {result_path}")

        # Check if file exists
        full_path = Path("..") / result_path.lstrip("/")
        if full_path.exists():
            file_size = full_path.stat().st_size
            print(f"  File size: {file_size / 1024:.1f} KB")
        else:
            print(f"  ⚠  Warning: Result file not found at {full_path}")

    except Exception as e:
        print(f"\n✗ API call failed: {e}")
        print("\nPossible issues:")
        print("  - API key is invalid or expired (OPENAI_API_KEY)")
        print("  - API quota exceeded")
        print("  - Model name is incorrect")
        print("  - Network connectivity issues")
        return

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
