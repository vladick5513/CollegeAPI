from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import User
from app.users.schemas import SUserRegister, SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register/")
async def register_user(user_data: SUserRegister):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": f'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="user_access_token", value=access_token,  httponly=True)
    return {"access_token": access_token, "refresh_token": None}

@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()


@router.post("/update_role/")
async def update_user_role(
        user_id: int, role_field: str, admin_user: User = Depends(get_current_admin_user)
):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    valid_roles = {"is_user", "is_student", "is_teacher", "is_admin", "is_super_admin"}
    if role_field not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недопустимая роль"
        )

    new_value = not getattr(user, role_field)
    await UsersDAO.update({"id": user_id}, **{role_field: new_value})
    return {"message": f"Роль '{role_field}' успешно обновлена на {new_value}"}

