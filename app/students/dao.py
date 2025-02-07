from sqlalchemy import select, event, update, delete
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_factory
from app.majors.models import Major
from app.students.models import Student

@event.listens_for(Student, "after_insert")
def receive_after_insert(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students = Major.count_students +1)
    )


class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_full_data(cls, student_id):
        async with async_session_factory() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            if not student_info:
                return None

            student_data = student_info.to_dict()
            student_data["major"] = student_info.major.major_name
            return student_data
    @classmethod
    async def add_student(cls, **student_data: dict):
        async with async_session_factory() as session:
            async with session.begin():
                new_student = Student(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id
