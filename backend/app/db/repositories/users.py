from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, role: str = "customer") -> User:
    hashed_password = get_password_hash(password)
    user = User(email=email, password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(
    db: Session,
    user_id: int,
    data: dict
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    return user

def change_password(
    db: Session,
    user_id: int,
    old_password: str,
    new_password: str
) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not verify_password(old_password, user.password):
        return False
    user.password = get_password_hash(new_password)
    db.commit()
    return True

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()