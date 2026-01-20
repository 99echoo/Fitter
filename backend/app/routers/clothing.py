from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Clothing
from app.schemas import ClothingListResponse, ClothingResponse

router = APIRouter(prefix="/api/clothing", tags=["clothing"])


@router.get("", response_model=ClothingListResponse)
def get_clothing_list(db: Session = Depends(get_db)):
    items = db.query(Clothing).all()
    return ClothingListResponse(
        items=[ClothingResponse.model_validate(item) for item in items]
    )


@router.get("/{clothing_id}", response_model=ClothingResponse)
def get_clothing(clothing_id: str, db: Session = Depends(get_db)):
    item = db.query(Clothing).filter(Clothing.id == clothing_id).first()
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Clothing not found")
    return ClothingResponse.model_validate(item)
