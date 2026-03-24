from fastapi import FastAPI
from config.database import Base, engine
from routes.student_route import router as student_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(student_router)