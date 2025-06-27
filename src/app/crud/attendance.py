from typing import List
from models.attendance import Attendance
from ..database import SessionLocal

def get_all_attendance() -> List[Attendance]:
    
    with SessionLocal() as db:
        return db.query(Attendance).order_by(Attendance.name).all()