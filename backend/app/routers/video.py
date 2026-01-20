from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TryOnRequest
from app.schemas import VideoGenerateRequest, VideoGenerateResponse
from app.services.kling_ai import KlingAIService

router = APIRouter(prefix="/api", tags=["video"])


@router.post("/generate-video", response_model=VideoGenerateResponse)
async def generate_video(
    request: VideoGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try_on_request = db.query(TryOnRequest).filter(
        TryOnRequest.id == request.request_id
    ).first()

    if not try_on_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if not try_on_request.result_image_url:
        raise HTTPException(
            status_code=400,
            detail="Try-on result not ready yet"
        )

    # Process video generation in background
    background_tasks.add_task(
        process_video_generation,
        str(try_on_request.id),
        try_on_request.result_image_url,
    )

    return VideoGenerateResponse(
        video_id=try_on_request.id,
        status="processing",
        video_url=None,
        duration=5,
        resolution="720p",
    )


async def process_video_generation(request_id: str, image_url: str):
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        service = KlingAIService()
        video_url = await service.generate_360_video(image_url)

        try_on_request = db.query(TryOnRequest).filter(
            TryOnRequest.id == request_id
        ).first()
        if try_on_request:
            try_on_request.video_url = video_url
            db.commit()
    except Exception as e:
        try_on_request = db.query(TryOnRequest).filter(
            TryOnRequest.id == request_id
        ).first()
        if try_on_request:
            try_on_request.error_message = f"Video generation failed: {str(e)}"
            db.commit()
    finally:
        db.close()
