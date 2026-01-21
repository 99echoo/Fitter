import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Clothing, TryOnRequest
from app.schemas import TryOnRequestResponse, TryOnResultResponse
from app.services.kling_ai import KlingAIService
from app.services.openai_image import OpenAIImageService, ClothingReference
from app.utils.file_handler import save_upload_file

router = APIRouter(prefix="/api", tags=["try-on"])


@router.post("/try-on", response_model=TryOnRequestResponse)
async def create_try_on(
    background_tasks: BackgroundTasks,
    face_image: UploadFile = File(...),
    body_image: UploadFile = File(...),
    clothing_ids: list[str] = Form(...),
    db: Session = Depends(get_db),
):
    requested_ids = [clothing_ids] if isinstance(clothing_ids, str) else clothing_ids

    normalized_ids: list[str] = []
    seen: set[str] = set()
    for item_id in requested_ids:
        if not item_id or item_id in seen:
            continue
        seen.add(item_id)
        normalized_ids.append(item_id)

    if not normalized_ids:
        raise HTTPException(status_code=400, detail="At least one clothing_id is required")

    clothing_items = db.query(Clothing).filter(Clothing.id.in_(normalized_ids)).all()
    clothing_by_id = {str(item.id): item for item in clothing_items}
    missing_ids = [item_id for item_id in normalized_ids if item_id not in clothing_by_id]
    if missing_ids:
        raise HTTPException(status_code=404, detail="Clothing not found")

    ordered_items = [clothing_by_id[item_id] for item_id in normalized_ids]
    seen_categories: set[str] = set()
    for item in ordered_items:
        if item.category in seen_categories:
            raise HTTPException(
                status_code=400,
                detail="Only one clothing item per category is allowed",
            )
        seen_categories.add(item.category)

    clothing_refs = [
        ClothingReference(
            path=item.image_url,
            category=item.category,
            name=item.name,
        )
        for item in ordered_items
    ]
    clothing_payload = [
        {"id": str(item.id), "category": item.category, "name": item.name}
        for item in ordered_items
    ]

    # Save uploaded files
    face_path = await save_upload_file(face_image, "face")
    body_path = await save_upload_file(body_image, "body")

    # Create try-on request
    try_on_request = TryOnRequest(
        clothing_id=ordered_items[0].id,
        clothing_items=clothing_payload,
        face_image_path=face_path,
        body_image_path=body_path,
        status="processing",
    )
    db.add(try_on_request)
    db.commit()
    db.refresh(try_on_request)

    # Process in background
    background_tasks.add_task(
        process_try_on,
        str(try_on_request.id),
        face_path,
        body_path,
        clothing_refs,
    )

    return TryOnRequestResponse(
        request_id=try_on_request.id,
        status=try_on_request.status,
        result_image_url=try_on_request.result_image_url,
        clothing_items=try_on_request.clothing_items,
        created_at=try_on_request.created_at,
    )


@router.get("/result/{request_id}", response_model=TryOnResultResponse)
def get_result(request_id: str, db: Session = Depends(get_db)):
    try_on_request = db.query(TryOnRequest).filter(TryOnRequest.id == request_id).first()
    if not try_on_request:
        raise HTTPException(status_code=404, detail="Request not found")

    return TryOnResultResponse(
        request_id=try_on_request.id,
        status=try_on_request.status,
        result_image_url=try_on_request.result_image_url,
        video_url=try_on_request.video_url,
        error_message=try_on_request.error_message,
        clothing_items=try_on_request.clothing_items,
        created_at=try_on_request.created_at,
        completed_at=try_on_request.completed_at,
    )


async def process_try_on(
    request_id: str,
    face_path: str,
    body_path: str,
    clothing_refs: list[ClothingReference],
):
    from app.database import SessionLocal
    from datetime import datetime

    db = SessionLocal()
    try:
        image_service = OpenAIImageService()
        result_url = await image_service.generate_try_on(face_path, body_path, clothing_refs)

        try_on_request = db.query(TryOnRequest).filter(TryOnRequest.id == request_id).first()
        if not try_on_request:
            return

        # Save image result first (video generation might take a while)
        try_on_request.result_image_url = result_url
        db.commit()

        try:
            video_service = KlingAIService()
            video_url = await video_service.generate_360_video(result_url)
        except Exception as e:
            try_on_request = db.query(TryOnRequest).filter(TryOnRequest.id == request_id).first()
            if try_on_request:
                try_on_request.status = "failed"
                try_on_request.error_message = f"Video generation failed: {str(e)}"
                db.commit()
            return

        try_on_request = db.query(TryOnRequest).filter(TryOnRequest.id == request_id).first()
        if try_on_request:
            try_on_request.status = "completed"
            try_on_request.video_url = video_url
            try_on_request.completed_at = datetime.now()
            db.commit()
    except Exception as e:
        try_on_request = db.query(TryOnRequest).filter(TryOnRequest.id == request_id).first()
        if try_on_request:
            try_on_request.status = "failed"
            try_on_request.error_message = str(e)
            db.commit()
    finally:
        db.close()
