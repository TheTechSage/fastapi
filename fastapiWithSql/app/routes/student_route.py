from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.students_schema import *
from controllers.student_controller import *

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse)
def create(data: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, data)


@router.get("/", response_model=list[StudentResponse])
def read_all(db: Session = Depends(get_db)):
    return get_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def read_one(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = update_student(db, student_id, data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    student = delete_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Deleted successfully"}