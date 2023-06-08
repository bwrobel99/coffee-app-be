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
    name: Mapped[str]
    description: Mapped[str]
    size: Mapped[CoffeeSize]
    price: Mapped[float]
    discount: Mapped[float] = mapped_column(default=0)
    favorite: Mapped[bool] = mapped_column(default=False)


class OrderCoffee(Base):
    __tablename__ = "orders_coffees"

    id: Mapped[IntPrimaryKey]

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    coffee_id: Mapped[int] = mapped_column(ForeignKey("coffees.id"))
    quantity: Mapped[int] = mapped_column(default=1)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[IntPrimaryKey]

    coffees: Mapped[list[Coffee]] = relationship(secondary="orders_coffees")
    order_coffees: Mapped[list[OrderCoffee]] = relationship()
