from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.config import settings

# Create SQLAlchemy engine
DATABASE_URL = settings.db.url 

engine = create_engine(DATABASE_URL, echo=True)  # echo=True to log SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()