"""Quick test for Nano Banana Pro API (Gemini 3 Pro Image)."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.nano_banana import NanoBananaService


async def main():
    print("=" * 60)
    print("Testing Nano Banana Pro API (Gemini 3 Pro Image)")
    print("=" * 60)
    print()

    # Initialize service
    try:
        service = NanoBananaService()
        print("✓ NanoBananaService initialized successfully")
        print(f"  Model: {service.model}")
    except Exception as e:
        print(f"✗ Failed to initialize service: {e}")
        return

    # Use test images from fixtures
    face_path = "tests/fixtures/sample_face.jpg"
    body_path = "tests/fixtures/sample_body.jpg"
    clothing_path = "tests/fixtures/sample_clothing.jpg"

    # Check if test images exist
    if not Path(face_path).exists():
        print(f"\n⚠  Missing test image: {face_path}")
        print("   Please add sample face and body photos to tests/fixtures/")
        print("   For now, using clothing image for all inputs (will fail but tests API)")
        face_path = clothing_path
        body_path = clothing_path

    print(f"\nTest inputs:")
    print(f"  Face: {face_path}")
    print(f"  Body: {body_path}")
    print(f"  Clothing: {clothing_path}")

    try:
        print("\n🚀 Generating virtual try-on image...")
        print("   (This may take 10-30 seconds)")

        result_path = await service.generate_try_on(
            face_path, body_path, clothing_path
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
        print("  - API key is invalid or expired")
        print("  - API quota exceeded")
        print("  - Model name is incorrect")
        print("  - Network connectivity issues")
        return

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
