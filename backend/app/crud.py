# crud.py
# CRUD(create, read, update, delete)를 수행하기 위한 모듈

from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name.like(f"{name}%")).all()


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
