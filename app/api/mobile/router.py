from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import SessionLocal
from app.models.media import Media
from pathlib import Path
from datetime import datetime

router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "Mobile API is working"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/media")
def list_media(user_id: int, date: str, db: Session = Depends(get_db)):
    """
    Mobile-friendly media list endpoint.
    Query params: user_id (int), date (YYYY-MM-DD)
    Returns list of media items with fields: id, original_name, url, media_type, created_at
    """
    try:
        dt = datetime.fromisoformat(date).date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

    medias = db.query(Media).filter(Media.user_id == user_id, Media.upload_date == dt, Media.is_deleted == False).all()
    result = []
    for m in medias:
        rel = Path(m.stored_path)
        url = f"/uploads/{rel.as_posix()}"
        result.append({
            "id": m.id,
            "original_name": m.original_name,
            "url": url,
            "media_type": m.media_type,
            "created_at": m.created_at,
        })
    return result
