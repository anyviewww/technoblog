# app/routers/complaints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/articles/{article_id}/complaints/", response_model=schemas.Complaint)
def create_complaint(article_id: int, complaint: schemas.ComplaintCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_complaint(db=db, complaint=complaint, article_id=article_id, user_id=current_user.id)
