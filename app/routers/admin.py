# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/admin/make_admin/{user_id}", response_model=schemas.User)
def make_admin(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.make_admin(db=db, user_id=user_id)

@router.get("/complaints/", response_model=List[schemas.Complaint])
def read_complaints(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    complaints = crud.get_complaints(db, skip=skip, limit=limit)
    return complaints

@router.post("/admin/ban_user/{user_id}", response_model=schemas.User)
def ban_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    return crud.ban_user(db=db, user_id=user_id)

@router.post("/admin/unban_user/{user_id}", response_model=schemas.User)
def unban_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    return crud.unban_user(db=db, user_id=user_id)

@router.post("/admin/move_article/{article_id}", response_model=schemas.Article)
def move_article(article_id: int, new_category: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    return crud.move_article(db=db, article_id=article_id, new_category=new_category)
