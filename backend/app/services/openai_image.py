import asyncio
import base64
import io
import logging
import mimetypes
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import aiofiles
import httpx
from openai import OpenAI
from PIL import Image, ImageOps, UnidentifiedImageError

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class PreparedImage:
    path: Path
    mime_type: str


@dataclass(frozen=True)
class ClothingReference:
    path: str
    category: str
    name: Optional[str] = None


class OpenAIImageService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        client_kwargs: dict[str, str] = {"api_key": settings.openai_api_key}
        if settings.openai_organization:
            client_kwargs["organization"] = settings.openai_organization
        if settings.openai_project:
            client_kwargs["project"] = settings.openai_project
        self.client = OpenAI(**client_kwargs)
        self.model = settings.openai_image_model
        self.max_image_side = settings.openai_image_max_side
        self.max_image_bytes = settings.openai_image_max_mb * 1024 * 1024
        self.jpeg_quality = settings.openai_image_jpeg_quality
        self.force_jpeg = settings.openai_image_force_jpeg
        self.output_size = settings.openai_image_output_size
        self.output_format = settings.openai_image_output_format.lower()
        self.output_quality = settings.openai_image_quality.lower()
        self.output_count = settings.openai_image_n
        self.max_input_images = settings.openai_image_max_inputs

    async def generate_try_on(
        self,
        face_image_path: str,
        body_image_path: str,
        clothing_image_paths: ClothingReference
        | list[ClothingReference]
        | str
        | list[str],
        model_image_path: Optional[str] = None,
    ) -> str:
        """
        Generate a virtual try-on image using OpenAI GPT Image.

        Args:
            face_image_path: Path to the face image
            body_image_path: Path to the body image
            clothing_image_paths: Clothing reference(s) (path + category)
            model_image_path: Optional model reference shot

        Returns:
            URL/path to the generated result image
        """
        clothing_items = self._normalize_clothing_inputs(clothing_image_paths)
        clothing_items = [item for item in clothing_items if item.path]
        max_inputs = max(self.max_input_images, 3)
        reserved_slots = 2 + (1 if model_image_path else 0)
        max_clothing = max(1, max_inputs - reserved_slots)
        if len(clothing_items) > max_clothing:
            logger.info(
                "Trimming clothing references from %d to %d", len(clothing_items), max_clothing
            )
            clothing_items = clothing_items[:max_clothing]

        if not clothing_items:
            raise ValueError("At least one clothing image is required")

        image_paths = [
            face_image_path,
            body_image_path,
            *(item.path for item in clothing_items),
        ]
        include_model_shot = False
        if model_image_path and len(image_paths) < max_inputs:
            image_paths.append(model_image_path)
            include_model_shot = True

        logger.info(
            "Preparing %d image(s) (clothing=%d, model_shot=%s)",
            len(image_paths),
            len(clothing_items),
            include_model_shot,
        )
        prepared_images = await asyncio.gather(
            *(self._prepare_image_file(path) for path in image_paths)
        )

        files = []
        try:
            for prepared in prepared_images:
                files.append(open(prepared.path, "rb"))

            prompt = self._build_prompt(
                clothing_items=clothing_items,
                include_model_shot=include_model_shot,
            )
            response = await asyncio.to_thread(self._edit_images, files, prompt)
        finally:
            for handle in files:
                try:
                    handle.close()
                except Exception:
                    pass
            for prepared in prepared_images:
                prepared.path.unlink(missing_ok=True)

        image_payloads = self._extract_image_payloads(response)
        if not image_payloads:
            raise RuntimeError("OpenAI Images API returned no image data")

        result_id = uuid.uuid4()
        result_paths = []
        extension = self._output_extension()
        result_dir = Path(settings.upload_dir) / "results"
        result_dir.mkdir(parents=True, exist_ok=True)

        for index, image_bytes in enumerate(image_payloads):
            suffix = f"_{index + 1}" if len(image_payloads) > 1 else ""
            result_filename = f"result_{result_id}{suffix}.{extension}"
            result_path = result_dir / result_filename

            async with aiofiles.open(result_path, "wb") as f:
                await f.write(image_bytes)

            result_paths.append(f"/uploads/results/{result_filename}")

        return result_paths[0]

    def _build_prompt(
        self, clothing_items: list[ClothingReference], include_model_shot: bool
    ) -> str:
        lines = [
            "You are a professional fashion photographer. Generate a photo of the person",
            "wearing the provided clothing item.",
            "",
            "Requirements:",
            "- Keep the person's face exactly as shown in the face reference image",
            "- Use the body proportions from the full-body reference image",
            "- Replace the clothing with the provided garment image(s)",
            "- Apply each clothing image according to its category (top, bottom, outerwear, dress)",
            "- Maintain a consistent pose: standing straight, front-facing, arms naturally at sides",
            "- Use a clean, neutral background (white or light gray)",
            "- Head-to-toe full body in frame: include the entire head and both feet",
            "- No cropping: ensure feet are fully visible with a small margin below the shoes",
            "- Professional studio lighting",
            "- High quality, realistic result",
            f"- Resolution: {self.output_size}",
        ]

        if len(clothing_items) > 1:
            lines.append("- Use all clothing reference images to capture accurate details")
        if include_model_shot:
            lines.append(
                "- Use the model reference shot for styling cues, but keep the user's face and body"
            )

        lines.extend(
            [
                "",
                "Reference images:",
                "1. Face photo: [Attached as image 1]",
                "2. Full body photo: [Attached as image 2]",
            ]
        )

        image_index = 3
        category_counts: dict[str, int] = {}
        for clothing in clothing_items:
            category_label = self._category_label(clothing.category)
            category_counts[category_label] = category_counts.get(category_label, 0) + 1
            category_index = category_counts[category_label]
            name_suffix = f" ({clothing.name})" if clothing.name else ""
            lines.append(
                f"{image_index}. {category_label} item {category_index}{name_suffix}: "
                f"[Attached as image {image_index}]"
            )
            image_index += 1

        if include_model_shot:
            lines.append(
                f"{image_index}. Model reference shot: [Attached as image {image_index}]"
            )

        return "\n".join(lines)

    def _category_label(self, category: str) -> str:
        return category or "Clothing"

    def _normalize_clothing_inputs(
        self,
        clothing_image_paths: ClothingReference
        | list[ClothingReference]
        | str
        | list[str],
    ) -> list[ClothingReference]:
        if isinstance(clothing_image_paths, ClothingReference):
            return [clothing_image_paths]
        if isinstance(clothing_image_paths, str):
            return [ClothingReference(path=clothing_image_paths, category="Clothing")]

        clothing_list = list(clothing_image_paths)
        if not clothing_list:
            return []
        if all(isinstance(item, ClothingReference) for item in clothing_list):
            return list(clothing_list)
        if all(isinstance(item, str) for item in clothing_list):
            return [
                ClothingReference(path=item, category="Clothing")
                for item in clothing_list
            ]

        raise ValueError("clothing_image_paths must be strings or ClothingReference objects")

    async def _prepare_image_file(self, path: str) -> PreparedImage:
        image_bytes = await self._read_image(path)
        logger.info("Loaded image %s (%0.1f KB)", path, len(image_bytes) / 1024)
        return await asyncio.to_thread(self._prepare_image_file_sync, image_bytes, path)

    def _prepare_image_file_sync(self, image_bytes: bytes, path: str) -> PreparedImage:
        mime_type = self._guess_mime_type(path)
        processed_bytes, processed_mime = self._process_image_bytes(image_bytes, mime_type)
        if len(processed_bytes) != len(image_bytes) or processed_mime != mime_type:
            logger.info(
                "Processed image %s: %0.1f KB -> %0.1f KB (%s -> %s)",
                path,
                len(image_bytes) / 1024,
                len(processed_bytes) / 1024,
                mime_type,
                processed_mime,
            )

        suffix = self._suffix_for_mime(processed_mime)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(processed_bytes)
            temp_path = Path(temp_file.name)

        return PreparedImage(path=temp_path, mime_type=processed_mime)

    def _process_image_bytes(self, image_bytes: bytes, mime_type: str) -> tuple[bytes, str]:
        should_process = self.force_jpeg or len(image_bytes) > self.max_image_bytes
        try:
            image = Image.open(io.BytesIO(image_bytes))
        except UnidentifiedImageError:
            return image_bytes, mime_type

        image = ImageOps.exif_transpose(image)
        max_side = max(image.size)
        needs_resize = max_side > self.max_image_side

        if not (should_process or needs_resize):
            return image_bytes, mime_type

        image = image.convert("RGB")
        if needs_resize:
            scale = self.max_image_side / float(max_side)
            new_size = (
                max(1, int(image.size[0] * scale)),
                max(1, int(image.size[1] * scale)),
            )
            image = image.resize(new_size, Image.LANCZOS)

        encoded = self._encode_jpeg_under_limit(image)
        return encoded, "image/jpeg"

    def _encode_jpeg_under_limit(self, image: Image.Image) -> bytes:
        qualities = [self.jpeg_quality, 80, 70, 60]
        for quality in qualities:
            encoded = self._encode_jpeg(image, quality)
            if len(encoded) <= self.max_image_bytes:
                return encoded

        encoded = self._encode_jpeg(image, 60)
        while len(encoded) > self.max_image_bytes and min(image.size) > 512:
            new_size = (
                max(1, int(image.size[0] * 0.85)),
                max(1, int(image.size[1] * 0.85)),
            )
            image = image.resize(new_size, Image.LANCZOS)
            encoded = self._encode_jpeg(image, 70)

        return encoded

    def _encode_jpeg(self, image: Image.Image, quality: int) -> bytes:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality, optimize=True)
        return buffer.getvalue()

    def _output_extension(self) -> str:
        if self.output_format == "jpeg":
            return "jpg"
        if self.output_format == "webp":
            return "webp"
        return "png"

    def _suffix_for_mime(self, mime_type: str) -> str:
        if mime_type == "image/png":
            return ".png"
        if mime_type == "image/webp":
            return ".webp"
        return ".jpg"

    def _edit_images(self, image_files: list, prompt: str):
        output_count = max(1, min(self.output_count, 5))
        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": output_count,
            "size": self.output_size,
        }
        if self.output_quality:
            payload["quality"] = self.output_quality
        if self.output_format:
            payload["output_format"] = self.output_format

        try:
            return self.client.images.edit(image=image_files, **payload)
        except TypeError as exc:
            if "unexpected keyword argument" in str(exc) and "image" in str(exc):
                return self.client.images.edit(images=image_files, **payload)
            raise

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

    def _extract_image_payloads(self, response) -> list[bytes]:
        data = response.get("data") if isinstance(response, dict) else getattr(response, "data", None)
        if not data:
            return []

        payloads: list[bytes] = []
        for item in data:
            if isinstance(item, dict):
                b64_json = item.get("b64_json")
            else:
                b64_json = getattr(item, "b64_json", None)
            if b64_json:
                payloads.append(base64.b64decode(b64_json))

        return payloads
