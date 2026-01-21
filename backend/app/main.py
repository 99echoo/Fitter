import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.database import Base, engine
from app.routers import clothing_router, try_on_router, video_router
import app.models  # noqa: F401

app = FastAPI(
    title="Fitter API",
    description="AI Virtual Try-On Service API",
    version="1.0.0",
)

# Ensure tables exist for local/dev usage unless tests skip init.
_skip_db_init = os.getenv("FITTER_SKIP_DB_INIT", "").lower() in {"1", "true", "yes"}
if not _skip_db_init:
    Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
uploads_path = Path(settings.upload_dir)
uploads_path.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_path)), name="uploads")

# Routers
app.include_router(clothing_router)
app.include_router(try_on_router)
app.include_router(video_router)


@app.get("/")
def root():
    return {"message": "Fitter API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
