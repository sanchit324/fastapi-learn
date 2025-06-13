from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .config import settings

DATABASE_USERNAME = settings.database_username
DATABASE_PASSWORD = settings.database_password
DATABASE_HOSTNAME = settings.database_hostname
DATABASE_PORT = settings.database_port
DATABASE_NAME = settings.database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error connecting to database: {e}")
    raise

def get_db():
    db = SessionLocal()
    try: 
        yield db    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()
        
        
# Database connection setup using psycopg2
'''
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='1234',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        time.sleep(2)  # Wait before retrying
'''
