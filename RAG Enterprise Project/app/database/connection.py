from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# database engine

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass