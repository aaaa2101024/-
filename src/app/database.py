from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent
DB_PATH = ROOT_PATH/"data"/"testDB.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()