from enum import Enum
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

IntPrimaryKey = Annotated[int, mapped_column(primary_key=True)]


class CoffeeSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class Coffee(Base):
    __tablename__ = "coffees"

    id: Mapped[IntPrimaryKey]
    name: str
    description: str
    size: CoffeeSize
    price: float
    discount: float = mapped_column(default=0)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[IntPrimaryKey]

    coffees: Mapped[list[Coffee]] = relationship(secondary="orders_coffees")


class OrderCoffee(Base):
    __tablename__ = "orders_coffees"

    id: Mapped[IntPrimaryKey]

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    coffee_id: Mapped[int] = mapped_column(ForeignKey("coffees.id"))
