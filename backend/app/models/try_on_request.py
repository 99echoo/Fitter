import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class TryOnRequest(Base):
    __tablename__ = "try_on_request"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    clothing_id = Column(String(64), ForeignKey("clothing.id"), nullable=False)
    clothing_items = Column(JSON)
    face_image_path = Column(String(500), nullable=False)
    body_image_path = Column(String(500), nullable=False)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    result_image_url = Column(String(500))
    video_url = Column(String(500))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    clothing = relationship("Clothing", backref="try_on_requests")
