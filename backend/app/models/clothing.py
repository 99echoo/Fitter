import uuid
from sqlalchemy import Column, String, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Clothing(Base):
    __tablename__ = "clothing"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # 상의, 하의, 아우터, 원피스, 기타
    image_url = Column(String(500), nullable=False)
    brand = Column(String(100))
    price = Column(Float, nullable=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
