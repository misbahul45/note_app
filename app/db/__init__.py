from app.core import get_settings
from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(get_settings().DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()