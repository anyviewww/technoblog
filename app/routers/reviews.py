# app/routers/reviews.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/articles/{article_id}/reviews/", response_model=schemas.Review)
def create_review(article_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_review(db=db, review=review, article_id=article_id, user_id=current_user.id)
