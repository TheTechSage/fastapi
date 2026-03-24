from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSON
from config.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=False)
    phone = Column(String)
    age = Column(String)
    gender  = Column(String)

    is_active = Column(Boolean, default=True)
    role = Column(String)

    address = Column(JSON)
    education = Column(JSON)
    skills = Column(JSON)
    