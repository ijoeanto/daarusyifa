from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

SQL_ALCHAMY_DATABASE_URL = f'mysql+pymysql://{os.environ.get("SQL_ALCHAMY_DATABASE_URL")}'
engine = create_engine(SQL_ALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
