# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db.db import get_db
# from db.middleware.auth_middleware import get_current_user
# from db.models.video import Video
# from db.models.user import User
# from db.models.comment import Comment
# from db.models.subscription import Subscription
# from db.models.like import Like
# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# router = APIRouter(prefix="/videos", tags=["Video Interactions"])

# # ----------- Schemas -----------

# class CommentRequest(BaseModel):
#     text: str

# class LikeRequest(BaseModel):
#     is_like: bool  # true = like, false = dislike

# # ----------- LIKE / DISLIKE -----------

# @router.post("/{video_id}/like")
# def like_video(
#     video_id: str,
#     data: LikeRequest,
#     user=Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     video = db.query(Video).filter(Video.id == video_id).first()
#     if not video:
#         raise HTTPException(404, "Video not found")

#     existing_like = db.query(Like).filter(
#         Like.user_id == user["sub"], Like.video_id == video_id
#     ).first()

#     if existing_like:
#         # toggle or update
#         if existing_like.is_like == data.is_like:
#             db.delete(existing_like)
#         else:
#             existing_like.is_like = data.is_like
#     else:
#         new_like = Like(
#             user_id=user["sub"],
#             video_id=video_id,
#             is_like=data.is_like,
#         )
#         db.add(new_like)

#     db.commit()
#     return {"message": "Like/Dislike updated successfully!"}

# # ----------- COMMENT -----------

# @router.post("/{video_id}/comment")
# def add_comment(
#     video_id: str,
#     data: CommentRequest,
#     user=Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     video = db.query(Video).filter(Video.id == video_id).first()
#     if not video:
#         raise HTTPException(404, "Video not found")

#     new_comment = Comment(
#         user_id=user["sub"],
#         video_id=video_id,
#         text=data.text,
#         created_at=datetime.utcnow()
#     )
#     db.add(new_comment)
#     db.commit()
#     db.refresh(new_comment)
#     return {"message": "Comment added!", "comment": new_comment.text}

# @router.get("/{video_id}/comment")
# def get_comments(video_id: str, db: Session = Depends(get_db)):
#     comments = (
#         db.query(Comment)
#         .filter(Comment.video_id == video_id)
#         .order_by(Comment.created_at.desc())
#         .all()
#     )
#     return [
#         {"user": c.user_id, "text": c.text, "created_at": c.created_at}
#         for c in comments
#     ]

# # ----------- SUBSCRIBE -----------

# @router.post("/{channel_id}/subscribe")
# def subscribe_channel(
#     channel_id: str,
#     user=Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     if user["sub"] == channel_id:
#         raise HTTPException(400, "You cannot subscribe to yourself!")

#     existing_sub = db.query(Subscription).filter(
#         Subscription.subscriber_id == user["sub"],
#         Subscription.channel_id == channel_id,
#     ).first()

#     if existing_sub:
#         db.delete(existing_sub)
#         action = "unsubscribed"
#     else:
#         db.add(
#             Subscription(subscriber_id=user["sub"], channel_id=channel_id)
#         )
#         action = "subscribed"

#     db.commit()
#     return {"message": f"Successfully {action}!"}

# # ----------- RELATED VIDEOS -----------

# @router.get("/{video_id}/related")
# def get_related_videos(video_id: str, db: Session = Depends(get_db)):
#     base_video = db.query(Video).filter(Video.id == video_id).first()
#     if not base_video:
#         raise HTTPException(404, "Video not found")

#     related = (
#         db.query(Video)
#         .filter(Video.id != video_id)
#         .filter(Video.title.ilike(f"%{base_video.title.split()[0]}%"))
#         .limit(5)
#         .all()
#     )

#     if not related:
#         return {"message": "No related videos found", "videos": []}

#     return {"videos": [
#         {
#             "id": v.id,
#             "title": v.title,
#             "description": v.description,
#             "thumbnail": f"https://{v.video_s3_key}/thumbnail.jpg"
#         } for v in related
#     ]}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from db.middleware.auth_middleware import get_current_user
from db.models.video import Video
from db.models.like_dislike import LikeDislike
from db.models.comment import Comment
from db.models.subscription import Subscription
from db.models.download import Download
from datetime import datetime
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/videos", tags=["Video Interactions"])

# ---------- Like / Dislike ----------
class LikeRequest(BaseModel):
    is_like: bool

@router.post("/{video_id}/like")
def like_video(video_id: str, data: LikeRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(LikeDislike).filter(
        LikeDislike.video_id == video_id, LikeDislike.user_id == user["sub"]
    ).first()

    if existing:
        if existing.is_like == data.is_like:
            db.delete(existing)  # toggle off
        else:
            existing.is_like = data.is_like
    else:
        db.add(LikeDislike(video_id=video_id, user_id=user["sub"], is_like=data.is_like))

    db.commit()
    return {"message": "Updated like/dislike"}

# ---------- Comments ----------
class CommentRequest(BaseModel):
    text: str

@router.post("/{video_id}/comment")
def post_comment(video_id: str, data: CommentRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    comment = Comment(id=str(uuid.uuid4()), user_id=user["sub"], video_id=video_id, text=data.text)
    db.add(comment)
    db.commit()
    return {"message": "Comment added"}

@router.get("/{video_id}/comment")
def get_comments(video_id: str, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.video_id == video_id).order_by(Comment.created_at.desc()).all()
    return [{"text": c.text, "user_id": c.user_id, "created_at": c.created_at} for c in comments]

# ---------- Subscribe ----------
@router.post("/{channel_id}/subscribe")
def subscribe_channel(channel_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if channel_id == user["sub"]:
        raise HTTPException(400, "Cannot subscribe to yourself")

    existing = db.query(Subscription).filter(
        Subscription.subscriber_id == user["sub"],
        Subscription.channel_id == channel_id
    ).first()

    if existing:
        db.delete(existing)
        action = "unsubscribed"
    else:
        db.add(Subscription(subscriber_id=user["sub"], channel_id=channel_id))
        action = "subscribed"

    db.commit()
    return {"message": f"Successfully {action}"}

# ---------- Download ----------
@router.post("/{video_id}/download")
def record_download(video_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(Download).filter(
        Download.video_id == video_id,
        Download.user_id == user["sub"]
    ).first()

    if record:
        record.count += 1
    else:
        db.add(Download(user_id=user["sub"], video_id=video_id))

    db.commit()
    return {"message": "Download recorded"}

# ---------- User videos ----------
@router.get("/user/{user_id}")
def get_user_videos(user_id: str, db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.user_id == user_id).all()
    return [v.to_dict() for v in videos]
