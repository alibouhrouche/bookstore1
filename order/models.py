from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(Enum("carted", "invoiced", "paid", "pending", "shipped", "cancelled"))
    owner_id = Column(Integer)
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    item_id = Column(Integer)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="order_items")
