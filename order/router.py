import requests
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/{order_id}")
def read_main(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id=order_id)


@app.get("/")
def read_all_main(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)


@app.post("/")
def create_main(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, order=order)
    return {"order": db_order}


@app.delete("/{order_id}")
def delete_main(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    crud.delete_order(db, order_id=order_id)
    return {"message": "Order deleted"}


@app.patch("/{order_id}")
@app.put("/{order_id}")
def update_main(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order = crud.update_order(db, order=order)
    return {"order": db_order}
