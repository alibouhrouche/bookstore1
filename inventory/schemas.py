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


class ItemBase(MyBaseModel):
    title: str
    description: str
    price: int
    stock: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True


ItemUpdate = Item.all_optional('ItemUpdate')
