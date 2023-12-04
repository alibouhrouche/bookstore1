from typing import Self

from pydantic import BaseModel, create_model


class MyBaseModel(BaseModel):
    @classmethod
    def all_optional(cls, name: str) -> type[Self]:
        """
        Creates a new model with the same fields, but all optional.

        Usage: SomeOptionalModel = SomeModel.all_optional('SomeOptionalModel')
        """
        return create_model(
            name,
            __base__=cls,
            **{name: (info.annotation, None) for name, info in cls.model_fields.items()}
        )


class OrderBase(MyBaseModel):
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


class OrderItemBase(MyBaseModel):
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


OrderUpdate = Order.all_optional('OrderUpdate')
