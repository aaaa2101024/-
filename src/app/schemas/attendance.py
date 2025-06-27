from pydantic import BaseModel
from datetime import datetime

class AttendanceResponse(BaseModel):
    id: int
    name : str
    status : str
    time: datetime

    class Config:
        orm_mode = True