from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Base, Coffee

from src.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/coffees")
def get_all_coffees(db: Session = Depends(get_db)):
    result = db.execute(select(Coffee)).scalars().all()
    
    return result
