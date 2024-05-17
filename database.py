from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_STRING_CONNECTION")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
