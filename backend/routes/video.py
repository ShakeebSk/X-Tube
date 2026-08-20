from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

# from backend.db.middleware.auth_middleware import get_current_user
from db.middleware.auth_middleware import get_current_user
from db.models.video import Video, ProcessingStatus, VisibilityStatus
from db.db import get_db
from sqlalchemy import or_
from db.redis_db import redis_client
import json

router = APIRouter()


@router.get("/all")
def get_all_videos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    all_videos = (
        db.query(Video)
        .filter(
            Video.is_processing == ProcessingStatus.COMPLETED,
            Video.visibility == VisibilityStatus.PUBLIC,
        )
        .all()
    )

    return all_videos


@router.get("/")
def get_video_info(
    video_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    cache_key = f"video:{video_id}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        print(cached_data)
        return json.loads(cached_data)

    video = (
        db.query(Video)
        .filter(
            Video.id == video_id,
            Video.is_processing == ProcessingStatus.COMPLETED,
            or_(
                Video.visibility == VisibilityStatus.PUBLIC,
                Video.visibility == VisibilityStatus.UNLISTED,
            ),
        )
        .first()
    )

    print(video.to_dict())

    redis_client.setex(cache_key,3600, json.dumps(video.to_dict()))

    return video

@router.put("/")
def update_video_by_id(id:str,db:Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == id).first()
    
    if not video:
        raise HTTPException(404,"Video not found")
    
    video.is_processing = ProcessingStatus.COMPLETED
    db.commit()
    db.refresh(video)
    
    return video
    
    
@router.get("/all")
def get_all_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.visibility == VisibilityStatus.PUBLIC).all()
    return [v.to_dict() for v in videos]

@router.get("/user/me")
def get_my_videos(user=Depends(get_current_user), db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.user_id == user["sub"]).all()
    return [v.to_dict() for v in videos]

@router.delete("/{video_id}")
def delete_video(video_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    v = db.query(Video).filter(Video.id == video_id).first()
    if not v:
        raise HTTPException(404, "Video not found")
    if v.user_id != user["sub"]:
        raise HTTPException(403, "Not allowed")
    db.delete(v)
    db.commit()
    # optionally also remove S3 objects and transcode entries (background)
    return {"message": "Deleted"}
