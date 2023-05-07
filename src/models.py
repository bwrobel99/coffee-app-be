from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

IntPrimaryKey = Annotated[int, mapped_column(primary_key=True)]


class Coffee(Base):
    __tablename__ = "coffees"

    id: Mapped[IntPrimaryKey]


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[IntPrimaryKey]

    coffees: Mapped[list[Coffee]] = relationship(secondary="orders_coffees")


class OrderCoffee(Base):
    __tablename__ = "orders_coffees"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    coffee_id: Mapped[int] = mapped_column(ForeignKey("coffees.id"), primary_key=True)
