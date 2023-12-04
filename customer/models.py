from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    status = Column(Enum("active", "inactive"))
    orders = Column(Integer)
