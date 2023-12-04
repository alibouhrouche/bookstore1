from typing import List

from pydantic import BaseModel


class OrderBase(BaseModel):
    title: str
    status: str
    owner_id: int


class OrderSimpleItem(BaseModel):
    id: int
    quantity: int


class OrderCreate(OrderBase):
    items: list[OrderSimpleItem]
    pass


class Order(OrderBase):
    id: int
    order_items: list
    
    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    item_id: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True
