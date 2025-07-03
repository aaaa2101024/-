from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from pathlib import Path
from create_table import Attendance

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR /"data"/"testDB.db"

engine = create_engine(f"sqlite:///{DB_PATH}",echo=True)

sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

from create_table import Base
def create_db_tables():
    Base.metadata.create_all(bind = engine)

def get_db() -> Session:
    db = sessionLocal()
    return db

db = get_db()

def re(id,status,time):
    with Session(engine, future=True) as db:
        user_a = db.get(Attendance, id)
        if user_a is not None:
            print(11111)
            user_a.status = status
            user_a.time = time
            db.commit()
