import asyncio
import mimetypes
import uuid
from pathlib import Path
from typing import Optional

from google import genai
from google.genai import types
import httpx
import aiofiles

from app.config import settings


class NanoBananaService:
    def __init__(self):
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is not set")
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model = settings.google_image_model

    async def generate_try_on(
        self,
        face_image_path: str,
        body_image_path: str,
        clothing_image_url: str,
    ) -> str:
        """
        Generate a virtual try-on image using Google Nano Banana Pro.

        Args:
            face_image_path: Path to the face image
            body_image_path: Path to the body image
            clothing_image_url: URL or path to the clothing image

        Returns:
            URL/path to the generated result image
        """
        # Read images with basic path/URL resolution.
        face_data, body_data, clothing_data = await asyncio.gather(
            self._read_image(face_image_path),
            self._read_image(body_image_path),
            self._read_image(clothing_image_url),
        )
        face_mime = self._guess_mime_type(face_image_path)
        body_mime = self._guess_mime_type(body_image_path)
        clothing_mime = self._guess_mime_type(clothing_image_url)

        prompt = """You are a professional fashion photographer. Generate a photo of the person
wearing the provided clothing item.

Requirements:
- Keep the person's face exactly as shown in the face reference image
- Use the body proportions from the full-body reference image
- Replace the clothing with the provided garment image
- Maintain a consistent pose: standing straight, front-facing, arms naturally at sides
- Use a clean, neutral background (white or light gray)
- Full body should be visible in the frame
- Professional studio lighting
- High quality, realistic result
- Resolution: 1024x1024

Reference images:
1. Face photo: [Attached as image 1]
2. Full body photo: [Attached as image 2]
3. Clothing item: [Attached as image 3]"""

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=face_data, mime_type=face_mime),
                    types.Part.from_bytes(data=body_data, mime_type=body_mime),
                    types.Part.from_bytes(data=clothing_data, mime_type=clothing_mime),
                ],
            )
        ]

        response = await asyncio.to_thread(self._generate_content_with_fallback, contents)

        # Save the generated image
        result_filename = f"result_{uuid.uuid4()}.jpg"
        result_path = Path(settings.upload_dir) / "results" / result_filename

        result_path.parent.mkdir(parents=True, exist_ok=True)

        image_bytes = self._extract_image_bytes(response)
        if not image_bytes:
            raise RuntimeError("Nano Banana API returned no image data")

        async with aiofiles.open(result_path, "wb") as f:
            await f.write(image_bytes)

        return f"/uploads/results/{result_filename}"

    async def _read_image(self, path: str) -> bytes:
        """Read image from file path or URL."""
        if path.startswith("http://") or path.startswith("https://"):
            async with httpx.AsyncClient() as client:
                response = await client.get(path, timeout=20.0)
                response.raise_for_status()
                return response.content

        resolved_path = self._resolve_local_path(path)
        with open(resolved_path, "rb") as f:
            return f.read()

    def _resolve_local_path(self, path: str) -> Path:
        if path.startswith("/uploads"):
            return Path(settings.upload_dir).parent / path.lstrip("/")

        if path.startswith("/"):
            repo_root = Path(__file__).resolve().parents[3]
            relative_path = path.lstrip("/")
            candidates = [
                repo_root / "frontend" / "public" / relative_path,
                repo_root / "public" / relative_path,
            ]
            for candidate in candidates:
                if candidate.exists():
                    return candidate

        return Path(path)

    def _guess_mime_type(self, path: str) -> str:
        mime_type, _ = mimetypes.guess_type(path)
        return mime_type or "image/jpeg"

    def _extract_image_bytes(self, response) -> Optional[bytes]:
        generated_images = getattr(response, "generated_images", None)
        if generated_images:
            for generated in generated_images:
                image = getattr(generated, "image", None)
                if image and getattr(image, "image_bytes", None):
                    return image.image_bytes

        candidates = getattr(response, "candidates", None)
        if candidates:
            content = candidates[0].content if candidates[0] else None
            parts = getattr(content, "parts", None) if content else None
            if parts:
                for part in parts:
                    inline_data = getattr(part, "inline_data", None)
                    if inline_data and getattr(inline_data, "data", None):
                        return inline_data.data

        return None

    def _generate_content_with_fallback(self, contents):
        configs = [
            types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                response_mime_type="image/jpeg",
            ),
            types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
            types.GenerateContentConfig(),
        ]

        last_exc = None
        for config in configs:
            try:
                return self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )
            except Exception as exc:
                last_exc = exc
                error_text = str(exc)
                retryable = (
                    "response_mime_type" in error_text
                    or "response modalities" in error_text
                    or "response_modalities" in error_text
                )
                if not retryable:
                    break

        raise RuntimeError(f"Nano Banana API request failed: {last_exc}") from last_exc
