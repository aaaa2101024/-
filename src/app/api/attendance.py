from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
from typing import List
from pathlib import Path
from fastapi import APIRouter
from schemas.attendance import AttendanceResponse


ROOT_PATH = Path(__file__).resolve().parent.parent.parent
DB_PATH = ROOT_PATH/"data"/"testDB.db"

router = APIRouter()

@router.get("/attendance", response_model=List[AttendanceResponse])
def get_attendance():
    try:
        with sqlite3.connect('../data/testDB.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
        
            cursor.execute("SELECT * FROM attendance")
            rows_from_db = cursor.fetchall()
        return [AttendanceResponse(name=row[0], status=row[1], time=row[2]) for row in rows_from_db]
    except sqlite3.Error as e:
        print({e})
        rows_from_db = []

# engine = create_engine("sqlite:///:attendance:")
# Base = declarative_base()
# Base.metadata.create_all(engine)
# SessionClass = sessionmaker(engine)
# session = SessionClass()