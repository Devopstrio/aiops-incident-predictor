import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

# Default Database connection URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost/aiops_db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency injection for SQLAlchemy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        # In production this should be handled by Alembic schema migrations
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database schema verified/initialized.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
