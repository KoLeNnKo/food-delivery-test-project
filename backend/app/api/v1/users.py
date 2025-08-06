from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.users import (
    get_user_by_id,
    update_user,
    change_password,
    get_users
)
from app.schemas.user import (
    UserInDB,
    UserUpdate,
    UserChangePassword
)
from app.core.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Не авторизован",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    }
)

@router.get(
    "/me",
    response_model=UserInDB,
    summary="Получить текущего пользователя",
    description="Возвращает данные авторизованного пользователя",
    responses={
        status.HTTP_200_OK: {
            "description": "Данные пользователя",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "role": "customer",
                        "address": "ул. Примерная, 123"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Пользователь не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
def get_me(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение информации о текущем авторизованном пользователе.
    Возвращает полные данные пользователя, включая email, роль и адрес.
    """
    db_user = get_user_by_id(db, user["id"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.patch(
    "/me",
    response_model=UserInDB,
    summary="Обновить данные пользователя",
    description="Обновляет информацию текущего пользователя (кроме пароля)",
    responses={
        status.HTTP_200_OK: {
            "description": "Данные успешно обновлены",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "updated@example.com",
                        "role": "customer",
                        "address": "Новый адрес"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Ошибка обновления",
            "content": {
                "application/json": {
                    "example": {"detail": "Update failed"}
                }
            }
        }
    }
)
def update_me(
    update_data: UserUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновление данных пользователя.
    Принимает только изменяемые поля (email, адрес).
    Пароль изменяется через отдельный метод.
    """
    updated_user = update_user(db, user["id"], update_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update failed"
        )
    return updated_user

@router.post(
    "/me/change-password",
    summary="Сменить пароль",
    description="Изменяет пароль текущего пользователя",
    responses={
        status.HTTP_200_OK: {
            "description": "Пароль успешно изменен",
            "content": {
                "application/json": {
                    "example": {"message": "Password updated"}
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Ошибка смены пароля",
            "content": {
                "application/json": {
                    "examples": {
                        "Неверный старый пароль": {"value": {"detail": "Old password is incorrect"}},
                        "Ошибка валидации": {"value": {"detail": "New password too weak"}}
                    }
                }
            }
        }
    }
)
def change_my_password(
    passwords: UserChangePassword,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Смена пароля пользователя.
    Требуется указать текущий пароль и новый пароль.
    Новый пароль должен соответствовать требованиям безопасности.
    """
    if not change_password(
        db, user["id"],
        passwords.old_password,
        passwords.new_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password change failed"
        )
    return {"message": "Password updated"}

@router.get(
    "/",
    response_model=List[UserInDB],
    summary="Получить список пользователей (admin)",
    description="Возвращает список всех пользователей (только для администраторов)",
    responses={
        status.HTTP_200_OK: {
            "description": "Список пользователей",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "email": "user1@example.com",
                            "role": "customer"
                        },
                        {
                            "id": 2,
                            "email": "admin@example.com",
                            "role": "admin"
                        }
                    ]
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Доступ запрещен",
            "content": {
                "application/json": {
                    "example": {"detail": "Forbidden"}
                }
            }
        }
    }
)
def admin_get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Получение списка пользователей с пагинацией.
    Доступно только для пользователей с ролью 'admin'.
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return get_users(db, skip, limit)