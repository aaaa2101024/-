from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker,Session
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///testDB.db", echo=True)

Base = automap_base()
Base.prepare(autoload_with=engine)

Attendance = Base.classes.attendance

session = Session(engine)
attendance_a = Attendance(name="tkuc",status="退勤",time="0000")

print(f"data: {attendance_a.name} {attendance_a.status}")




# Base = declarative_base()

# class Attendance(Base):
#     __tablename__ = "attendance"

#     name = Column(String)
#     status = Column(String)
#     time = Column(String)

# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

