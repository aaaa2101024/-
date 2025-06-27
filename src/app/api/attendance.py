from fastapi import APIRouter
from typing import List
from schemas.attendance import AttendanceResponse
from crud.attendance import get_all_attendance

router = APIRouter()

@router.get("/attendance", response_model=List[AttendanceResponse])
def read_attendance_endpoint():
    return get_all_attendance()