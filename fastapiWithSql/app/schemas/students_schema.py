from pydantic import BaseModel
from typing import List, Dict, Optional

class StudentBase(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    gender: str
    is_active: bool
    role: str
    address: Dict
    education: Dict
    skills: List[str]

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    is_active: Optional[bool]
    role: Optional[str]
    address: Optional[Dict]
    education: Optional[Dict]
    skills: Optional[List[str]]

class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True