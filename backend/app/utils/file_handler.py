import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.config import settings


async def save_upload_file(file: UploadFile, prefix: str = "") -> str:
    """
    Save an uploaded file to the uploads directory.

    Args:
        file: The uploaded file
        prefix: Optional prefix for the filename

    Returns:
        The path to the saved file
    """
    # Generate unique filename
    ext = Path(file.filename).suffix if file.filename else ".jpg"
    filename = f"{prefix}_{uuid.uuid4()}{ext}"

    # Create upload directory if it doesn't exist
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)

    file_path = upload_path / filename

    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    return str(file_path)


def get_file_url(file_path: str) -> str:
    """Convert a file path to a URL."""
    return f"/uploads/{Path(file_path).name}"
