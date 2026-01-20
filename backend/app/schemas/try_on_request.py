from pydantic import BaseModel
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime


TryOnStatus = Literal["pending", "processing", "completed", "failed"]


class TryOnRequestBase(BaseModel):
    clothing_id: UUID


class TryOnRequestCreate(TryOnRequestBase):
    face_image_path: str
    body_image_path: str


class TryOnRequestResponse(BaseModel):
    request_id: UUID
    status: TryOnStatus
    result_image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TryOnResultResponse(BaseModel):
    request_id: UUID
    status: TryOnStatus
    result_image_url: Optional[str] = None
    video_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VideoGenerateRequest(BaseModel):
    request_id: UUID


class VideoGenerateResponse(BaseModel):
    video_id: UUID
    status: TryOnStatus
    video_url: Optional[str] = None
    duration: int = 5
    resolution: str = "720p"
