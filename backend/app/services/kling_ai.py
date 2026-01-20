import uuid
from pathlib import Path

import httpx

from app.config import settings


class KlingAIService:
    def __init__(self):
        self.api_key = settings.kling_api_key
        self.base_url = "https://api.klingai.com/v1"

    async def generate_360_video(self, image_url: str) -> str:
        """
        Generate a 360-degree rotation video from an image using Kling AI.

        Args:
            image_url: URL or path to the source image

        Returns:
            URL/path to the generated video
        """
        prompt = """Create a smooth 360-degree rotation video of this person.
- Camera slowly rotates around the subject
- Subject remains stationary in the center
- Maintain consistent lighting throughout
- Duration: 5 seconds
- Smooth, professional motion"""

        # Read the image
        image_data = self._read_image(image_url)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Create video generation request
        async with httpx.AsyncClient() as client:
            # Submit the generation task
            response = await client.post(
                f"{self.base_url}/image2video",
                headers=headers,
                json={
                    "model": "kling-v2-1",
                    "prompt": prompt,
                    "image": image_data,
                    "duration": 5,
                    "resolution": "720p",
                },
                timeout=60.0,
            )

            if response.status_code != 200:
                raise Exception(f"Kling AI API error: {response.text}")

            result = response.json()
            task_id = result.get("task_id")

            # Poll for completion
            video_url = await self._wait_for_completion(client, headers, task_id)

            # Download and save the video
            video_response = await client.get(video_url)
            video_filename = f"video_{uuid.uuid4()}.mp4"
            video_path = Path(settings.upload_dir) / "videos" / video_filename

            video_path.parent.mkdir(parents=True, exist_ok=True)

            with open(video_path, "wb") as f:
                f.write(video_response.content)

            return f"/uploads/videos/{video_filename}"

    async def _wait_for_completion(
        self,
        client: httpx.AsyncClient,
        headers: dict,
        task_id: str,
        max_attempts: int = 60,
    ) -> str:
        """Poll for video generation completion."""
        import asyncio

        for _ in range(max_attempts):
            response = await client.get(
                f"{self.base_url}/tasks/{task_id}",
                headers=headers,
            )

            if response.status_code != 200:
                raise Exception(f"Failed to check task status: {response.text}")

            result = response.json()
            status = result.get("status")

            if status == "completed":
                return result.get("video_url")
            elif status == "failed":
                raise Exception(f"Video generation failed: {result.get('error')}")

            await asyncio.sleep(5)

        raise Exception("Video generation timed out")

    def _read_image(self, path: str) -> str:
        """Read image and convert to base64."""
        import base64

        if path.startswith("http"):
            import httpx
            response = httpx.get(path)
            data = response.content
        else:
            # Handle local path
            if path.startswith("/uploads"):
                path = str(Path(settings.upload_dir).parent / path.lstrip("/"))
            with open(path, "rb") as f:
                data = f.read()

        return base64.b64encode(data).decode("utf-8")
