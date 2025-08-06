from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Хеш пароля
    role = Column(Enum("customer", "courier", "admin", name="user_roles"))
    address = Column(String, nullable=True)

    orders = relationship("Order", back_populates="user")