from sqlalchemy.orm import Session
from . import models, schemas

def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()

def get_news_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.News).offset(skip).limit(limit).all()

def create_news(db: Session, news: schemas.NewsCreate):
    db_news = models.News(title=news.title, content=news.content)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def delete_news(db: Session, news_id: int):
    db_news = db.query(models.News).filter(models.News.id == news_id).first()
    if db_news:
        db.delete(db_news)
        db.commit()
    return db_news

def update_news(db: Session, news_id: int, updated_news: schemas.NewsCreate):
    db_news = db.query(models.News).filter(models.News.id == news_id).first()
    if db_news:
        db_news.title = updated_news.title
        db_news.content = updated_news.content
        db.commit()
        db.refresh(db_news)
    return db_news