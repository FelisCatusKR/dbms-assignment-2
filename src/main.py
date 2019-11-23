from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from starlette import status
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import FileResponse

# DB를 다루기 위한 모듈
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base

app = FastAPI()

# 어플리케이션 시작 시, Base에 저장시킨 메타데이터에 따라
# DB 테이블 생성 (DB에 테이블이 있을 시 무시됨)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)


"""
# 어플리케이션 종료 시, DB의 모든 테이블 삭제 (디버깅용)
@app.on_event("shutdown")
async def shutdown():
    Base.metadata.drop_all(engine)
"""

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Create
@app.post(
    "/api/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user


# Read (Finding user(s) with query)
@app.get("/api/users/", response_model=schemas.SearchResult)
def read_users(
    name: str = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Query is null"
        )
    users = crud.get_user_by_name(db=db, name=name, skip=skip, limit=limit)
    return users


# Read (One user)
@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


# Update
@app.put("/api/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    return db_user


# Delete
@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    return db_user



@app.get("/robots.txt")
def robots():
    return FileResponse("/app/robots.txt", status_code=status.HTTP_304_NOT_MODIFIED, filename="robots.txt", media_type="text/plain")