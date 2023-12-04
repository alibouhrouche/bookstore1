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


@app.get("/{order_id}/{item_id}")
def read_main_order():
    return {"message": "Hello World"}


@app.get("/")
def read_all_main(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)


@app.post("/")
def create_main(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, order=order)
    data = requests.post("http://127.0.0.1:8000/inventory/items", json=[x.id for x in order.items])
    if data.status_code != 200:
        raise HTTPException(status_code=500, detail=data.text)
    for x in order.items:
        val = data.json()["items"][str(x.id)]
        item = models.OrderItem(
            order_id=db_order.id,
            item_id=x.id,
            title=val["title"],
            description=val["description"],
            price=val["price"],
            quantity=x.quantity,
        )
        if val["stock"] < x.quantity:
            raise HTTPException(status_code=500, detail="Not enough stock")
        crud.add_item_to_order(db, item, db_order.id)
    requests.post("http://127.0.0.1:8000/customers/" + str(db_order.owner_id) + "/order")
    return {"order": db_order}


@app.delete("/{order_id}")
def delete_main(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    crud.delete_order(db, order_id=order_id)
    return {"message": "Order deleted"}
