from fastapi import APIRouter

from app.majors.dao import MajorsDAO
from app.majors.schemas import SMajorsAdd, SMajorsUpdDesc

router = APIRouter(prefix="/majors", tags=["Работа с факультетами"])

@router.post("/add/")
async def add_major(major: SMajorsAdd) -> dict:
    check = await MajorsDAO.add(**major.model_dump())
    if check:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        return {"message": "Ошибка при добавлении факультета!"}

@router.put("/update_description/")
async def update_major_description(major: SMajorsUpdDesc) -> dict:
    check = await MajorsDAO.update(filter_by={"major_name": major.major_name},
                                   major_description=major.major_description)
    if check:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        return {"message": "Ошибка при обновлении описания факультета!"}


