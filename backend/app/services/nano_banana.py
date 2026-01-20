import base64
import uuid
from pathlib import Path

from google import genai
from google.genai import types

from app.config import settings


class NanoBananaService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model = "gemini-2.0-flash-exp-image-generation"

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
        # Read images and convert to base64
        face_data = self._read_image(face_image_path)
        body_data = self._read_image(body_image_path)
        clothing_data = self._read_image(clothing_image_url)

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
                    types.Part.from_bytes(data=face_data, mime_type="image/jpeg"),
                    types.Part.from_bytes(data=body_data, mime_type="image/jpeg"),
                    types.Part.from_bytes(data=clothing_data, mime_type="image/jpeg"),
                ],
            )
        ]

        generate_content_config = types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
            response_mime_type="image/jpeg",
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        )

        # Save the generated image
        result_filename = f"result_{uuid.uuid4()}.jpg"
        result_path = Path(settings.upload_dir) / "results" / result_filename

        result_path.parent.mkdir(parents=True, exist_ok=True)

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                with open(result_path, "wb") as f:
                    f.write(part.inline_data.data)
                break

        return f"/uploads/results/{result_filename}"

    def _read_image(self, path: str) -> bytes:
        """Read image from file path or URL."""
        if path.startswith("http"):
            import httpx
            response = httpx.get(path)
            return response.content
        else:
            with open(path, "rb") as f:
                return f.read()
