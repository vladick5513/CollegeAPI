from fastapi import FastAPI
from app.students.router import router as router_students
from app.majors.router import router as router_majors
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_users)