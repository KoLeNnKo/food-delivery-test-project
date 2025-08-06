from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(
        "created", "paid", "cooking", "delivering", "delivered", "canceled",
        name="order_status"
    ), default="created")
    total = Column(Float)  # Сумма заказа
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # Связи
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    quantity = Column(Integer, default=1)
    price_at_order = Column(Float)  # Фиксация цены на момент заказа

    # Связи
    order = relationship("Order", back_populates="items")
    dish = relationship("Dish", back_populates="order_items")