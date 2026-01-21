from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from uuid import UUID


ClothingCategory = Literal["상의", "하의", "아우터", "원피스", "기타"]


class ClothingBase(BaseModel):
    name: str
    category: ClothingCategory
    image_url: str
    brand: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


class ClothingCreate(ClothingBase):
    pass


class ClothingResponse(ClothingBase):
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def normalize_id(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value

    class Config:
        from_attributes = True


class ClothingListResponse(BaseModel):
    items: list[ClothingResponse]
