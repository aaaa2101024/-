from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    status = Column(String)
    time = Column(DateTime)