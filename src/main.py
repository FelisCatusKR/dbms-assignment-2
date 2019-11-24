# main.py
# 주소의 Routing을 포함한 기본 작동을 다루는 모듈

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# DB를 다루기 위한 모듈
from . import crud, models, schemas
from .database import SessionLocal, engine

# Base에 저장시킨 메타데이터에 따라 DB 테이블 생성
# (DB에 테이블이 있을 시 무시됨)
models.Base.metadata.create_all(engine)

# 백엔드를 구성하기 위한 기본 변수들을 선언
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 검색 봇들을 차단하는 Robots.txt
@app.get("/robots.txt")
def robots():
    return FileResponse(
        "/app/robots.txt", filename="robots.txt", media_type="text/plain"
    )


# CRUD 작업에 사용할 DB 세션을 선언하는 기저함수
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# # 어플리케이션 종료 시, DB의 모든 테이블 삭제 (디버깅용)
# @app.on_event("shutdown")
# async def shutdown():
#     Base.metadata.drop_all(engine)


# Root에 접근 시, templates 폴더에 있는 index.html을 반환한다.
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Create
@app.post(
    "/api/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


# Read (Finding user(s) with query)
@app.get("/api/users/", response_model=schemas.SearchResult)
def read_users(
    name: str = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # (skip만큼 건너뛰고 limit만큼만 가져온다)
    return crud.get_users_by_name(db=db, name=name, skip=skip, limit=limit)


responses = {404: {"model": schemas.Message}}

# Read (One user)
@app.get("/api/users/{user_id}", response_model=schemas.User, responses=responses)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    # 해당 user_id를 가진 유저가 없을 경우,
    # status code 404를 반환한다
    if db_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    else:
        return db_user


# Update
@app.put("/api/users/{user_id}", response_model=schemas.User, responses=responses)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    # 삭제하고자 하는 user_id에 해당하는 유저가 없을 경우,
    # status code 404를 반환한다
    if db_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    else:
        return crud.update_user(db=db, user_id=user_id, user=user)


# Delete
@app.delete(
    "/api/users/{user_id}", response_model=schemas.DeleteResult, responses=responses
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 삭제하고자 하는 user_id에 해당하는 유저가 없을 경우,
    # status code 404를 반환한다
    if crud.get_user(db=db, user_id=user_id) is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )

    result = crud.delete_user(db=db, user_id=user_id)
    return {"result": result}
