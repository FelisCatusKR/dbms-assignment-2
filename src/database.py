from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

user = environ["POSTGRES_USER"]
password = environ["POSTGRES_PASSWORD"]
host = environ["POSTGRES_HOST"]
dbname = environ["POSTGRES_DB"]
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{dbname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
