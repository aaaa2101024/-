from sqlalchemy import create_engine , Column,Integer,String, DateTime
from sqlalchemy.orm import declarative_base,Mapped,mapped_column
from datetime import  datetime
from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///./testDB.db",echo=True)


Base = declarative_base()

class Attendance(Base):
    __tablename__ = "Attendance"
    id:Mapped[int] = Column(Integer,primary_key=True,nullable=False)
    name:Mapped[str] = Column(String,nullable=False)
    status:Mapped[str] = Column(String,nullable=False)
    time:Mapped[str]= Column(String,nullable=False)
    
    def __repr__(self):
        return f"<Attendance(id='{self.id}',name='{self.name}',status='{self.status}'.time='{self.time}')>"

# SessionClass = sessionmaker(bind=engine)
# # session = SessionClass()

# user_a = SessionClass().query(Attendance).get(1)
# user_a.status = "zaisitu"
# SessionClass().commit()

