"""Quick test for Kling AI Image-to-Video API."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.kling_ai import KlingAIService


async def main():
    print("=" * 60)
    print("Testing Kling AI Image-to-Video API")
    print("=" * 60)
    print()

    # Initialize service
    try:
        service = KlingAIService()
        print("✓ KlingAIService initialized successfully")
        print(f"  Base URL: {service.base_url}")
        print(f"  Model: {service.model_name}")
        print(f"  Mode: {service.mode}, Duration: {service.duration}s")
    except Exception as e:
        print(f"✗ Failed to initialize service: {e}")
        return

    # Use a test result image (or clothing image as fallback)
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

    test_image_paths = [
        "uploads/results/result_*.png",  # From previous GPT-Image test
        "uploads/results/result_*.jpg",
        "/Fullshot.jpeg",
        "/Model_CUT.png",
        "/faceshot.jpeg",
    ]

    image_path = None
    for pattern in test_image_paths:
        if "*" in pattern:
            # Try to find any matching file
            import glob
            matches = glob.glob(pattern)
            if matches:
                image_path = matches[0]
                break
        else:
            if path_exists(pattern):
                image_path = pattern
                break

    if not image_path:
        print("\n⚠  No test image found!")
        print("   Please run test_gpt_image.py first to generate a result image,")
        print("   or ensure sample_clothing.jpg exists in tests/fixtures/")
        return

    print(f"\nTest input: {image_path}")

    try:
        print("\n🚀 Generating 360-degree rotation video...")
        print("   (This may take 1-5 minutes depending on queue)")
        print(f"   Model: {service.model_name}")

        video_path = await service.generate_360_video(image_path)

        print(f"\n✓ Success! Video saved to: {video_path}")

        # Check if file exists
        full_path = Path("..") / video_path.lstrip("/")
        if full_path.exists():
            file_size = full_path.stat().st_size
            print(f"  File size: {file_size / 1024 / 1024:.1f} MB")
        else:
            print(f"  ⚠  Warning: Video file not found at {full_path}")

    except Exception as e:
        print(f"\n✗ API call failed: {e}")
        print("\nPossible issues:")
        print("  - API key is invalid or not set")
        print("  - Model name may not be correct")
        print("  - Kling API is unavailable")
        print("  - Network connectivity issues")
        print("  - API quota exceeded")
        print("\nTroubleshooting:")
        print("  1. Check your KLING_ACCESS_KEY/KLING_SECRET_KEY in .env")
        print("  2. Verify the base URL and model_name from Kling docs")
        return

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
