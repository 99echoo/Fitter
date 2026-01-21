import asyncio
import base64
import hashlib
import hmac
import json
import time
import uuid
from pathlib import Path
import httpx

from app.config import settings


class KlingAIService:
    def __init__(self):
        self.access_key = settings.kling_access_key or settings.kling_api_key
        self.secret_key = settings.kling_secret_key
        if not self.access_key or not self.secret_key:
            raise ValueError("KLING_ACCESS_KEY/KLING_SECRET_KEY is not set")
        self.base_url = settings.kling_base_url.rstrip("/")
        self.model_name = settings.kling_model_name
        self.mode = settings.kling_mode
        self.duration = settings.kling_duration

    async def generate_360_video(self, image_url: str) -> str:
        """
        Generate a 360-degree rotation video from an image using Kling AI.

        Args:
            image_url: URL or path to the source image

        Returns:
            URL/path to the generated video
        """
        prompt = "\n".join(
            [
                "Use the uploaded reference image as the exact model.",
                "The person, face, body proportions, hairstyle, clothing, and overall appearance must remain identical to the reference image.",
                "Do not change the model's identity, outfit, or styling.",
                "",
                "The model in the reference image performs a smooth, natural full 360-degree turn on the runway.",
                "The model starts facing forward, slowly rotates clockwise, completes one full spin, and returns to the original front-facing pose.",
                "",
                "CAMERA & FRAMING",
                "",
                "Medium full-body shot",
                "Camera fixed at eye level",
                "Centered composition",
                "No camera movement, no shake",
                "Subtle cinematic depth of field",
                "",
                "MOTION TIMELINE",
                "",
                "0.0-1.5s: Model stands still, facing forward",
                "1.5-4.0s: Model slowly turns clockwise, completing a full 360-degree rotation",
                "            Arms relaxed, posture natural",
                "            Clothing and fabric move naturally with the body",
                "4.0-5.0s: Model finishes the turn and holds a confident final pose",
                "",
                "STYLE & LIGHTING",
                "",
                "Same lighting and mood as the reference image",
                "Clean studio or runway background",
                "Soft, directional studio lighting emphasizing fabric texture",
                "High-fashion editorial tone",
                "",
                "CONSTRAINTS",
                "",
                "Do NOT change face or identity",
                "Do NOT change outfit, color, or fabric",
                "Do NOT add accessories",
                "Only body rotation and natural fabric motion are allowed",
                "One continuous shot, seamless motion",
            ]
        )

        image_input = await self._prepare_image_input(image_url)

        payload = {
            "model_name": self.model_name,
            "mode": self.mode,
            "duration": self.duration,
            "image": image_input,
            "prompt": prompt,
        }

        headers = {
            "Authorization": f"Bearer {self._build_jwt_token()}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/videos/image2video",
                headers=headers,
                json=payload,
                timeout=60.0,
            )
            result = self._safe_json(response)
            if response.status_code >= 400 or result.get("code") not in (0, "0", None):
                raise RuntimeError(self._format_error(response, result))

            task_id = self._extract_task_id(result)
            if not task_id:
                raise RuntimeError(f"Kling AI API returned no task_id: {result}")

            video_url = await self._wait_for_completion(client, headers, task_id)

            video_response = await client.get(video_url, timeout=60.0)
            video_response.raise_for_status()

        video_filename = f"video_{uuid.uuid4()}.mp4"
        video_path = Path(settings.upload_dir) / "videos" / video_filename
        video_path.parent.mkdir(parents=True, exist_ok=True)

        with open(video_path, "wb") as f:
            f.write(video_response.content)

        return f"/uploads/videos/{video_filename}"

    async def _prepare_image_input(self, path: str) -> str:
        """Return base64 for local files or URL for remote images."""
        if path.startswith("http://") or path.startswith("https://"):
            return path

        resolved_path = self._resolve_local_path(path)
        data = Path(resolved_path).read_bytes()
        if len(data) > 10 * 1024 * 1024:
            raise ValueError("Input image exceeds 10MB Kling AI limit")
        return base64.b64encode(data).decode("utf-8")

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

    def _build_jwt_token(self, ttl_seconds: int = 3600) -> str:
        """Build a short-lived JWT token signed with the Kling secret key."""
        now = int(time.time())
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "iss": self.access_key,
            "nbf": now,
            "exp": now + ttl_seconds,
            "iat": now,
        }

        header_b64 = self._b64url_json(header)
        payload_b64 = self._b64url_json(payload)
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            signing_input,
            hashlib.sha256,
        ).digest()
        signature_b64 = self._b64url(signature)
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    def _b64url_json(self, data: dict) -> str:
        return self._b64url(json.dumps(data, separators=(",", ":")).encode("utf-8"))

    def _b64url(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    async def _wait_for_completion(
        self,
        client: httpx.AsyncClient,
        headers: dict,
        task_id: str,
        max_attempts: int = 60,
    ) -> str:
        """Poll for video generation completion."""
        for _ in range(max_attempts):
            response = await client.get(
                f"{self.base_url}/v1/videos/image2video/{task_id}",
                headers=headers,
                timeout=60.0,
            )
            result = self._safe_json(response)
            if response.status_code >= 400 or result.get("code") not in (0, "0", None):
                raise RuntimeError(self._format_error(response, result))

            data = result.get("data") or {}
            status = data.get("task_status")

            if status == "succeed":
                video_url = self._extract_video_url(data)
                if not video_url:
                    raise RuntimeError(f"Kling AI API returned no video URL: {result}")
                return video_url
            if status == "failed":
                message = data.get("task_status_msg") or "Unknown Kling AI failure"
                raise RuntimeError(f"Kling AI video generation failed: {message}")

            await asyncio.sleep(5)

        raise RuntimeError("Video generation timed out")

    def _extract_task_id(self, result: dict) -> str:
        data = result.get("data") or {}
        return data.get("task_id") or ""

    def _extract_video_url(self, data: dict) -> str:
        task_result = data.get("task_result") or {}
        videos = task_result.get("videos") or []
        if videos:
            return str(videos[0].get("url") or "")
        return ""

    def _safe_json(self, response: httpx.Response) -> dict:
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}

    def _format_error(self, response: httpx.Response, result: dict) -> str:
        status = response.status_code
        return f"Kling AI API error ({status}): {result}"
