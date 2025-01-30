from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk, str_uniq, str_null_true


class Major(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    count_students: Mapped[int] = mapped_column(server_default=text("0"))