from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now())