# database.py
# PostgreSQL과의 통신을 위한 SQLAlchemy Session을 만드는 모듈

# Docker 이미지에 등록된 환경 변수를 추출하기 위한 모듈
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = environ["POSTGRES_USER"]
password = environ["POSTGRES_PASSWORD"]
host = environ["POSTGRES_HOST"]
dbname = environ["POSTGRES_DB"]
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{dbname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
