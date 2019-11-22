# crud.py
# CRUD(create, read, update, delete)를 수행하기 위한 모듈

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()


def get_user_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    first_name: str = name[0]
    q = db.query(models.User).filter(models.User.name.like(f"{name}%"))
    return {
        # 파싱한 쿼리의 성
        "first_name": first_name,
        # 파싱한 쿼리의 성과 같은 성을 가진 사람의 수
        "first_name_number": db.query(models.User)
        .filter(models.User.name.like(f"{first_name}%"))
        .count(),
        # 파싱한 쿼리와 이름의 앞부분 일치하는 사람의 수
        "number": q.count(),
        # 파싱한 쿼리와 이름의 앞부분이 일치하는 사람의 목록
        # (skip만큼 건너뛰고 limit만큼만 가져온다)
        "user_list": q.offset(skip).limit(limit).all(),
    }


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(name=user.name, phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserBase):
    db_user = db.query(models.User).filter_by(id=user_id).first()
    db_user.name = user.name
    db_user.phone_number = user.phone_number
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = models.User()
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
