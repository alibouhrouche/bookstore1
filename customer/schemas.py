from typing import Optional, Self

from pydantic import BaseModel, main, create_model


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


class CustomerBase(MyBaseModel):
    name: str
    email: str
    phone: str
    address: str
    status: str
    orders: int


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


CustomerUpdate = CustomerBase.all_optional('CustomerUpdate')
