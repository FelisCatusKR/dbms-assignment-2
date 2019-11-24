# crud.py
# CRUD(create, read, update, delete)를 수행하기 위한 모듈

from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()


def get_users_by_name(db: Session, name: str, skip: int, limit: int):
    # 검색할 이름이 비어있는 경우, 전체 유저 출력을 쿼리하며, 성이 같은 사람을 찾지 않음
    if name is None:
        q = db.query(models.User)
        first_name = ""
        first_name_number = 0
    # 검색할 이름이 있는 경우, 해당 이름으로 시작하는 유저 출력을 쿼리하며,
    # 동시에 성이 같은 사람의 수를 찾음
    else:
        q = db.query(models.User).filter(models.User.name.like(f"{name}%"))
        first_name = name[0]
        first_name_number = (
            db.query(models.User)
            .filter(models.User.name.like(f"{first_name}%"))
            .count()
        )

    return {
        "first_name": first_name,
        "first_name_number": first_name_number,
        "number": q.count(),
        "user_list": q.offset(skip).limit(limit).all(),
    }


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(name=user.name, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserBase):
    db_user = get_user(db=db, user_id=user_id)
    db_user.name = user.name
    db_user.phone = user.phone
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    if get_user(db=db, user_id=user_id) is not None:
        return False
    else:
        return True
