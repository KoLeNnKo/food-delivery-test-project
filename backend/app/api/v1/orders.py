from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.order import Order, OrderItem
from app.services.cart import CartService
from app.core.security import get_current_user
from typing import Dict

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Не авторизован",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    }
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый заказ",
    description="Создает заказ из товаров в корзине пользователя и очищает корзину",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Заказ успешно создан",
            "content": {
                "application/json": {
                    "example": {"order_id": 5, "message": "Order created successfully"}
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Корзина пуста",
            "content": {
                "application/json": {
                    "example": {"detail": "Cart is empty"}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Блюдо не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Dish not found"}
                }
            }
        }
    }
)
def create_order(
        db: Session = Depends(get_db),
        user: Dict = Depends(get_current_user)
):
    """
    Создание заказа из текущего содержимого корзины.

    Процесс:
    1. Проверяет наличие товаров в корзине
    2. Создает новый заказ со статусом 'created'
    3. Переносит все позиции из корзины в заказ
    4. Очищает корзину
    5. Возвращает ID созданного заказа

    Требуется авторизация.
    """
    cart = CartService.get_cart(user["id"])
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )

    try:
        # Создаем заказ
        order = Order(user_id=user["id"], status="created")
        db.add(order)
        db.commit()

        # Добавляем позиции
        for dish_id, quantity in cart.items():
            item = OrderItem(
                order_id=order.id,
                dish_id=int(dish_id),
                quantity=int(quantity)
            )
            db.add(item)

        db.commit()
        CartService.clear_cart(user["id"])

        return {
            "order_id": order.id,
            "message": "Order created successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )