from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from datetime import datetime
from uuid import UUID


TryOnStatus = Literal["pending", "processing", "completed", "failed"]


class ClothingItemReference(BaseModel):
    id: str
    category: str
    name: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def normalize_id(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value


class TryOnRequestBase(BaseModel):
    clothing_id: str


class TryOnRequestCreate(TryOnRequestBase):
    face_image_path: str
    body_image_path: str


class TryOnRequestResponse(BaseModel):
    request_id: str
    status: TryOnStatus
    result_image_url: Optional[str] = None
    clothing_items: Optional[list[ClothingItemReference]] = None
    created_at: datetime

    @field_validator("request_id", mode="before")
    @classmethod
    def normalize_request_id(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value

    class Config:
        from_attributes = True


class TryOnResultResponse(BaseModel):
    request_id: str
    status: TryOnStatus
    result_image_url: Optional[str] = None
    video_url: Optional[str] = None
    error_message: Optional[str] = None
    clothing_items: Optional[list[ClothingItemReference]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    @field_validator("request_id", mode="before")
    @classmethod
    def normalize_request_id(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value

    class Config:
        from_attributes = True


class VideoGenerateRequest(BaseModel):
    request_id: str


class VideoGenerateResponse(BaseModel):
    video_id: str
    status: TryOnStatus
    video_url: Optional[str] = None
    duration: int = 5
    resolution: str = "720p"
