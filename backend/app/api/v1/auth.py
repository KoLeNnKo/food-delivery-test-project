from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import Token, UserCreate, UserLogin
from app.db.repositories.users import get_user_by_email, create_user
from app.core.security import create_access_token, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=Token,
    summary="Регистрация нового пользователя",
    description="Создает учетную запись пользователя и возвращает JWT-токен",
    responses={
        status.HTTP_200_OK: {
            "description": "Успешная регистрация",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Ошибка регистрации",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already registered"}
                }
            }
        }
    }
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация пользователя с обязательными полями:
    - email: valid email address
    - password: пароль длиной не менее 6 символов
    """
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = create_user(db, user_data.email, user_data.password)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    "/login",
    response_model=Token,
    summary="Аутентификация пользователя",
    description="Проверяет учетные данные и возвращает JWT-токен",
    responses={
        status.HTTP_200_OK: {
            "description": "Успешная аутентификация",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Неверные учетные данные",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
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
                                "loc": ["body", "username"],
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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя по email и паролю.
    Возвращает JWT-токен для доступа к защищенным эндпоинтам.
    """
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}