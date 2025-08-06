from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.services.cart import CartService
from app.core.security import get_current_user
from typing import Dict, Any

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Не авторизован",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    }
)


@router.post(
    "/add/{dish_id}/{quantity}",
    summary="Добавить блюдо в корзину",
    description="Добавляет указанное количество блюда в корзину пользователя",
    responses={
        status.HTTP_200_OK: {
            "description": "Блюдо успешно добавлено",
            "content": {"application/json": {"example": {"message": "Dish added to cart"}}}
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Некорректные данные",
            "content": {"application/json": {"example": {"detail": "Invalid dish ID"}}}
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Блюдо не найдено",
            "content": {"application/json": {"example": {"detail": "Dish not found"}}}
        }
    }
)
def add_to_cart(
        dish_id: int = Path(..., title="ID блюда", example=1, gt=0),
        quantity: int = Path(..., title="Количество", example=2, gt=0),
        user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Добавляет блюдо в корзину пользователя.

    Параметры:
    - dish_id: ID блюда из меню (должен быть > 0)
    - quantity: Количество порций (должно быть > 0)

    Требуется авторизация.
    """
    try:
        CartService.add_to_cart(user["id"], dish_id, quantity)
        return {"message": "Dish added to cart"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "",
    summary="Просмотр корзины",
    description="Возвращает текущее содержимое корзины пользователя",
    response_model=Dict[int, int],
    responses={
        status.HTTP_200_OK: {
            "description": "Содержимое корзины",
            "content": {"application/json": {"example": {1: 2, 3: 1}}}
        }
    }
)
def view_cart(
        user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Возвращает содержимое корзины в формате:
    {
        "dish_id": quantity,
        ...
    }

    Требуется авторизация.
    """
    return CartService.get_cart(user["id"])