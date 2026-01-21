"""End-to-end test: GPT-image try-on -> Kling AI video."""
import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.openai_image import OpenAIImageService, ClothingReference
from app.services.kling_ai import KlingAIService


def path_exists(repo_root: Path, path: str) -> bool:
    if path.startswith("/"):
        relative_path = path.lstrip("/")
        candidates = [
            repo_root / "frontend" / "public" / relative_path,
            repo_root / "public" / relative_path,
        ]
        return any(candidate.exists() for candidate in candidates)
    return Path(path).exists()


def pick_existing_path(repo_root: Path, paths: list[str]) -> str:
    for candidate in paths:
        if path_exists(repo_root, candidate):
            return candidate
    return paths[-1]


def resolve_upload_path(path: str) -> Path:
    if path.startswith("/uploads"):
        return Path(path.lstrip("/"))
    return Path(path)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    print("=" * 60)
    print("End-to-end test: GPT-image -> Kling AI")
    print("=" * 60)
    print()

    try:
        openai_service = OpenAIImageService()
        print("[OK] OpenAIImageService initialized")
    except Exception as exc:
        print(f"[ERR] OpenAIImageService init failed: {exc}")
        return

    try:
        kling_service = KlingAIService()
        print("[OK] KlingAIService initialized")
    except Exception as exc:
        print(f"[ERR] KlingAIService init failed: {exc}")
        return

    repo_root = Path(__file__).resolve().parents[2]

    face_candidates = ["/faceshot.jpeg", "tests/fixtures/sample_face.jpg"]
    body_candidates = ["/Fullshot.jpeg", "tests/fixtures/sample_body.jpg"]
    clothing_candidates = ["/Model_CUT.png", "tests/fixtures/sample_clothing.jpg"]

    face_path = pick_existing_path(repo_root, face_candidates)
    body_path = pick_existing_path(repo_root, body_candidates)
    clothing_path = pick_existing_path(repo_root, clothing_candidates)

    if not (
        path_exists(repo_root, face_path)
        and path_exists(repo_root, body_path)
        and path_exists(repo_root, clothing_path)
    ):
        print("\n[WARN] Missing test images.")
        print("Add files to tests/fixtures/ or /public to run the full test.")
        return

    print("\nTest inputs:")
    print(f"  Face: {face_path}")
    print(f"  Body: {body_path}")
    print(f"  Clothing: {clothing_path}")

    try:
        print("\n[RUN] Generating try-on image...")
        result_path = await openai_service.generate_try_on(
            face_path,
            body_path,
            [ClothingReference(path=clothing_path, category="상의")],
        )
        print(f"[OK] Try-on result: {result_path}")
    except Exception as exc:
        print(f"[ERR] Try-on generation failed: {exc}")
        return

    result_file = resolve_upload_path(result_path)
    if result_file.exists():
        print(f"[OK] Result file exists: {result_file}")
    else:
        print(f"[WARN] Result file not found at: {result_file}")

    try:
        print("\n[RUN] Generating Kling AI video...")
        video_path = await kling_service.generate_360_video(result_path)
        print(f"[OK] Video result: {video_path}")
    except Exception as exc:
        print(f"[ERR] Video generation failed: {exc}")
        return

    video_file = resolve_upload_path(video_path)
    if video_file.exists():
        print(f"[OK] Video file exists: {video_file}")
    else:
        print(f"[WARN] Video file not found at: {video_file}")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
