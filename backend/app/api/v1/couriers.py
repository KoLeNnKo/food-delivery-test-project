from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.order import Order
from app.core.security import get_current_user
from typing import List, Dict, Any

router = APIRouter(
    prefix="/couriers",
    tags=["Couriers"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Не авторизован",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    }
)


@router.get(
    "/orders",
    summary="Получить доступные заказы",
    description="Возвращает список заказов со статусом 'paid', доступных для доставки",
    response_model=List[Dict[str, Any]],
    responses={
        status.HTTP_200_OK: {
            "description": "Список доступных заказов",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 5,
                            "status": "paid",
                            "total": 25.99,
                            "created_at": "2023-01-01T12:00:00"
                        }
                    ]
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Доступ запрещен",
            "content": {
                "application/json": {
                    "example": {"detail": "Only for couriers"}
                }
            }
        }
    }
)
def get_available_orders(
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Получение списка заказов, готовых к доставке.

    Доступно только для пользователей с ролью 'courier'.
    Возвращает заказы со статусом 'paid'.
    """
    if user["role"] != "courier":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for couriers"
        )

    orders = db.query(Order).filter(Order.status == "paid").all()
    return orders


@router.post(
    "/orders/{order_id}/accept",
    summary="Принять заказ на доставку",
    description="Позволяет курьеру принять заказ на доставку",
    responses={
        status.HTTP_200_OK: {
            "description": "Заказ успешно принят",
            "content": {
                "application/json": {
                    "example": {"message": "Order accepted"}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Доступ запрещен",
            "content": {
                "application/json": {
                    "example": {"detail": "Only for couriers"}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Заказ не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Order not found"}
                }
            }
        }
    }
)
def accept_order(
        order_id: int = Path(..., title="ID заказа", example=1, gt=0),
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Принятие заказа на доставку курьером.

    Параметры:
    - order_id: ID заказа (должен быть > 0)

    Доступно только для пользователей с ролью 'courier'.
    Меняет статус заказа на 'delivering' и устанавливает courier_id.
    """
    if user["role"] != "courier":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for couriers"
        )

    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    order.status = "delivering"
    order.courier_id = user["id"]
    db.commit()
    return {"message": "Order accepted"}