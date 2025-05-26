from app.core import get_settings
from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(get_settings().DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
