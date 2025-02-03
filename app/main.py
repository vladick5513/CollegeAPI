from fastapi import FastAPI
from app.students.router import router as router_students

app = FastAPI()

app.include_router(router_students)