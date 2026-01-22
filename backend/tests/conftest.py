"""
Test fixtures for Fitter backend tests.
"""
import os
import pytest
import asyncio
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, AsyncMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

os.environ.setdefault("FITTER_SKIP_DB_INIT", "1")

from app.main import app
from app.database import Base, get_db
from app.models.clothing import Clothing
from app.models.try_on_request import TryOnRequest


# Database fixtures

@pytest.fixture(scope="function")
def test_db() -> Generator[Session, None, None]:
    """
    Create a test database session with cleanup.
    Uses an in-memory SQLite database for fast isolated tests.
    """
    # Create in-memory SQLite database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(test_db: Session) -> TestClient:
    """
    Create a FastAPI test client with test database.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Mock service fixtures

@pytest.fixture
def mock_openai_image():
    """Mock OpenAIImageService for testing."""
    mock_service = Mock()
    mock_service.generate_try_on = AsyncMock(
        return_value="/uploads/results/test_result.png"
    )
    return mock_service


@pytest.fixture
def mock_kling_ai():
    """Mock KlingAIService for testing."""
    mock_service = Mock()
    mock_service.generate_360_video = AsyncMock(
        return_value="/uploads/videos/test_video.mp4"
    )
    return mock_service


# Sample data fixtures

@pytest.fixture
def sample_clothing(test_db: Session) -> Clothing:
    """Create a sample clothing item in the test database."""
    clothing = Clothing(
        id="test-clothing-1",
        name="Test T-Shirt",
        category="top",
        image_url="/amazon_fashion/B0711VZG7W.jpg",
        brand="Test Brand",
        price=29.99
    )
    test_db.add(clothing)
    test_db.commit()
    test_db.refresh(clothing)
    return clothing


@pytest.fixture
def sample_images(tmp_path: Path) -> dict:
    """
    Create sample image files for testing.
    Returns paths to face, body, and clothing test images.
    """
    # Create temporary image files
    face_path = tmp_path / "face.jpg"
    body_path = tmp_path / "body.jpg"
    clothing_path = tmp_path / "clothing.jpg"

    # Write minimal JPEG headers (valid but empty images)
    jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9'

    face_path.write_bytes(jpeg_header)
    body_path.write_bytes(jpeg_header)
    clothing_path.write_bytes(jpeg_header)

    return {
        "face": str(face_path),
        "body": str(body_path),
        "clothing": str(clothing_path),
    }


@pytest.fixture
def sample_try_on_request(test_db: Session, sample_clothing: Clothing) -> TryOnRequest:
    """Create a sample try-on request in the test database."""
    request = TryOnRequest(
        id="test-request-1",
        clothing_id=sample_clothing.id,
        face_image_path="/uploads/face_test.png",
        body_image_path="/uploads/body_test.png",
        status="pending"
    )
    test_db.add(request)
    test_db.commit()
    test_db.refresh(request)
    return request


# Utility fixtures

@pytest.fixture
def temp_upload_dir(tmp_path: Path) -> Path:
    """Create a temporary upload directory for tests."""
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    (upload_dir / "results").mkdir()
    (upload_dir / "videos").mkdir()
    return upload_dir


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
