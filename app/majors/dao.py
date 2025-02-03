from app.dao.base import BaseDAO
from app.majors.models import Major


class StudentDAO(BaseDAO):
    model = Major