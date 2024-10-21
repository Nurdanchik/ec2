from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Import List from typing
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# Инициализация базы данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создание новости
@app.post("/news/", response_model=schemas.News)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    return crud.create_news(db=db, news=news)

# Получение списка новостей
@app.get("/news/", response_model=List[schemas.News])  # Use List[schemas.News]
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_news_list(db=db, skip=skip, limit=limit)

# Получение новости по id
@app.get("/news/{news_id}", response_model=schemas.News)
def read_news_by_id(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news(db=db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return db_news

# Обновление новости
@app.put("/news/{news_id}", response_model=schemas.News)
def update_news(news_id: int, news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.update_news(db=db, news_id=news_id, updated_news=news)
    if db_news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return db_news

# Удаление новости
@app.delete("/news/{news_id}", response_model=schemas.News)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.delete_news(db=db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return db_news

origins = [
    # "http://localhost:3000",
    "http://100.24.66.165/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)