from sqlalchemy.orm import Session
from models.student_model import Student

# CREATE
def create_student(db: Session, data):
    student = Student(**data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


# READ ALL
def get_students(db: Session):
    return db.query(Student).all()


# READ ONE
def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


# UPDATE
def update_student(db: Session, student_id: int, data):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


# DELETE
def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return None

    db.delete(student)
    db.commit()
    return student