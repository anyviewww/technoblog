# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from sqlalchemy import desc

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    db_article = models.Article(**article.dict(), owner_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_articles(db: Session, skip: int = 0, limit: int = 10, category: Optional[str] = None, sort_by: Optional[str] = None):
    query = db.query(models.Article)
    if category:
        query = query.filter(models.Article.category == category)
    if sort_by:
        if sort_by == "title":
            query = query.order_by(models.Article.title)
        elif sort_by == "-title":
            query = query.order_by(desc(models.Article.title))
        elif sort_by == "date":
            query = query.order_by(models.Article.created_at)
        elif sort_by == "-date":
            query = query.order_by(desc(models.Article.created_at))
    return query.offset(skip).limit(limit).all()

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    db.delete(db_article)
    db.commit()
    return db_article

def create_comment(db: Session, comment: schemas.CommentCreate, article_id: int, user_id: int):
    db_comment = models.Comment(**comment.dict(), article_id=article_id, owner_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db.delete(db_comment)
    db.commit()
    return db_comment

def create_complaint(db: Session, complaint: schemas.ComplaintCreate, article_id: int, user_id: int):
    db_complaint = models.Complaint(**complaint.dict(), article_id=article_id, user_id=user_id)
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def get_complaints(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Complaint).offset(skip).limit(limit).all()

def create_review(db: Session, review: schemas.ReviewCreate, article_id: int, user_id: int):
    db_review = models.Review(**review.dict(), article_id=article_id, user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def ban_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_banned = True
    db.commit()
    db.refresh(db_user)
    return db_user

def unban_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_banned = False
    db.commit()
    db.refresh(db_user)
    return db_user

def move_article(db: Session, article_id: int, new_category: str):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    db_article.category = new_category
    db.commit()
    db.refresh(db_article)
    return db_article
