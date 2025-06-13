from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.config import settings

# Test database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Create test engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_tables():
    """Create all tables in the test database."""
    Base.metadata.create_all(bind=engine)

def drop_test_tables():
    """Drop all tables from the test database."""
    Base.metadata.drop_all(bind=engine)

def get_test_db():
    """Get a database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
