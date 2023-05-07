from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db, SessionLocal
from src.models import Base, Coffee, CoffeeSize

from src.database import engine

sizes = [val for val in CoffeeSize]

fixtures = [
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
            session.add_all(fixtures)
            session.commit()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/coffees")
def get_all_coffees(db: Session = Depends(get_db)):
    result = db.execute(select(Coffee)).scalars().all()

    return result
