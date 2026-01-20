import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Clothing, TryOnRequest
from app.schemas import TryOnRequestResponse, TryOnResultResponse
from app.services.nano_banana import NanoBananaService
from app.utils.file_handler import save_upload_file

router = APIRouter(prefix="/api", tags=["try-on"])


@router.post("/try-on", response_model=TryOnRequestResponse)
async def create_try_on(
    background_tasks: BackgroundTasks,
    face_image: UploadFile = File(...),
    body_image: UploadFile = File(...),
    clothing_id: str = Form(...),
    db: Session = Depends(get_db),
):
    # Validate clothing exists
    clothing = db.query(Clothing).filter(Clothing.id == clothing_id).first()
    if not clothing:
        raise HTTPException(status_code=404, detail="Clothing not found")

    # Save uploaded files
    face_path = await save_upload_file(face_image, "face")
    body_path = await save_upload_file(body_image, "body")

    # Create try-on request
    try_on_request = TryOnRequest(
        clothing_id=clothing_id,
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
        clothing.image_url,
    )

    return TryOnRequestResponse(
        request_id=try_on_request.id,
        status=try_on_request.status,
        result_image_url=try_on_request.result_image_url,
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
        created_at=try_on_request.created_at,
        completed_at=try_on_request.completed_at,
    )


async def process_try_on(
    request_id: str,
    face_path: str,
    body_path: str,
    clothing_url: str,
):
    from app.database import SessionLocal
    from datetime import datetime

    db = SessionLocal()
    try:
        service = NanoBananaService()
        result_url = await service.generate_try_on(face_path, body_path, clothing_url)

        try_on_request = db.query(TryOnRequest).filter(TryOnRequest.id == request_id).first()
        if try_on_request:
            try_on_request.status = "completed"
            try_on_request.result_image_url = result_url
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
