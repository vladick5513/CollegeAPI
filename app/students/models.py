from datetime import date

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_uniq, str_null_true


class Student(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    enrollment_year: Mapped[int]
    course: Mapped[int]
    special_notes: Mapped[str_null_true]
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=False)

    major: Mapped["Major"] = relationship("Major", back_populates="students")


    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}),"
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r}")

    def __repr__(self):
        return str(self)