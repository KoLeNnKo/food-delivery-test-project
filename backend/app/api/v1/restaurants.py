from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.restaurant import Restaurant, Dish
from app.schemas.restaurant import RestaurantCreate, DishCreate
from app.core.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Не авторизован",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    }
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать ресторан",
    description="Создает новый ресторан (только для администраторов)",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Ресторан успешно создан",
            "content": {
                "application/json": {
                    "example": {"message": "Restaurant created", "restaurant_id": 1}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Доступ запрещен",
            "content": {
                "application/json": {
                    "example": {"detail": "Only admin can create restaurants"}
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "name"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def create_restaurant(
        restaurant: RestaurantCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """
    Создание нового ресторана в системе.

    Требования:
    - Только пользователи с ролью 'admin' могут создавать рестораны
    - Название ресторана должно быть уникальным
    - Локация должна быть в формате 'широта,долгота'
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create restaurants"
        )

    db_restaurant = Restaurant(name=restaurant.name, location=restaurant.location)
    db.add(db_restaurant)
    db.commit()
    return {
        "message": "Restaurant created",
        "restaurant_id": db_restaurant.id
    }


@router.get(
    "/",
    summary="Получить список ресторанов",
    description="Возвращает список всех ресторанов с их основными данными",
    response_model=List[RestaurantCreate],
    responses={
        status.HTTP_200_OK: {
            "description": "Список ресторанов",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Burger King",
                            "location": "55.751244,37.618423"
                        }
                    ]
                }
            }
        }
    }
)
def get_restaurants(db: Session = Depends(get_db)):
    """
    Получение списка всех доступных ресторанов.

    Возвращает:
    - ID ресторана
    - Название
    - Локацию (широта,долгота)
    """
    return db.query(Restaurant).all()


@router.post(
    "/dishes/",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить блюдо в меню",
    description="Добавляет новое блюдо в меню ресторана",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Блюдо успешно добавлено",
            "content": {
                "application/json": {
                    "example": {"message": "Dish added", "dish_id": 5}
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "price"],
                                "msg": "ensure this value is greater than 0",
                                "type": "value_error.number.not_gt",
                                "ctx": {"limit_value": 0}
                            }
                        ]
                    }
                }
            }
        }
    }
)
def add_dish(
        dish: DishCreate,
        db: Session = Depends(get_db)
):
    """
    Добавление нового блюда в меню ресторана.

    Параметры:
    - restaurant_id: ID ресторана
    - name: Название блюда
    - description: Описание (опционально)
    - price: Цена (должна быть > 0)
    """
    db_dish = Dish(**dish.dict())
    db.add(db_dish)
    db.commit()
    return {
        "message": "Dish added",
        "dish_id": db_dish.id
    }