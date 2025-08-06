from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    location_lat = Column(Float)  # Широта
    location_lon = Column(Float)  # Долгота
    is_active = Column(Boolean, default=True)

    # Связь с блюдами (1 ко многим)
    dishes = relationship("Dish", back_populates="restaurant")

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)  # Decimal в реальном проекте
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    # Связи
    restaurant = relationship("Restaurant", back_populates="dishes")
    order_items = relationship("OrderItem", back_populates="dish")