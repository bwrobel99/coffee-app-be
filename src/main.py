from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db, SessionLocal
from src.models import Base, Coffee, CoffeeSize, Order, OrderCoffee

from src.database import engine

sizes = [val for val in CoffeeSize]

coffee_fixtures = [
    Coffee(
        name=f"Coffee {n}",
        description=f"Description {n}",
        size=sizes[n % 3],
        price=10 + n,
        discount=n,
    )
    for n in range(15)
]


@asynccontextmanager
async def lifespan(_):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        if not session.execute(select(Coffee)).scalars().all():
            session.add_all(coffee_fixtures)
            session.commit()
            order_fixtures = [
                Order(
                    coffees=[
                        coffee for coffee in coffee_fixtures if (coffee.id - n) % 4 == 0
                    ]
                )
                for n in range(3)
            ]
            session.add_all(order_fixtures)
            session.commit()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/coffees")
def get_all_coffees(favorite: bool = False, db: Session = Depends(get_db)):
    query = select(Coffee)
    if favorite:
        query = query.where(Coffee.favorite.is_(True))

    result = db.execute(query).scalars().all()

    return result


@app.get("/coffees/{id}")
def get_coffee(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Coffee).where(Coffee.id == id)).scalar()

    return result


@app.post("/coffees/{id}/set-favorite", status_code=200)
def set_coffee_favorite(id: int, db: Session = Depends(get_db)):
    coffee = db.execute(select(Coffee).where(Coffee.id == id)).scalar()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    coffee.favorite = False if coffee.favorite else True

    db.add(coffee)
    db.commit()


@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    result = db.execute(select(Order)).scalars().all()

    return [
        {
            "id": o.id,
            "coffees": [
                {**coffee.__dict__, "quantity": o.order_coffees[idx].quantity}
                for idx, coffee in enumerate(o.coffees)
            ],
        }
        for o in result
    ]


@app.post("/orders")
def add_order(payload: dict, db: Session = Depends(get_db)):
    order = Order(
        order_coffees=[
            OrderCoffee(coffee_id=item["id"], quantity=item["quantity"])
            for item in payload["coffees"]
        ]
    )
    db.add(order)
    db.commit()

    return {
        "id": order.id,
        "coffees": [
            {**coffee.__dict__, "quantity": order.order_coffees[idx].quantity}
            for idx, coffee in enumerate(order.coffees)
        ],
    }
