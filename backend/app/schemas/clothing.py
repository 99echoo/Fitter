from pydantic import BaseModel
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
    id: UUID

    class Config:
        from_attributes = True


class ClothingListResponse(BaseModel):
    items: list[ClothingResponse]
