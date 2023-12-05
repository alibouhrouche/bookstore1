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


@app.get("/")
def read_main(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return {"customers": customers}


@app.post("/")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.create_customer(db=db, customer=customer)
    return {"customer": db_customer}


@app.get("/{customer_id}")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer": db_customer}


@app.patch("/{customer_id}")
@app.put("/{customer_id}")
def update_customer(
    customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    db_customer = crud.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.orders = db_customer.orders if customer.orders is None else customer.orders
    customer.name = db_customer.name if customer.name is None else customer.name
    customer.email = db_customer.email if customer.email is None else customer.email
    customer.phone = db_customer.phone if customer.phone is None else customer.phone
    customer.address = db_customer.address if customer.address is None else customer.address
    db_customer = crud.update_customer(db=db, id=customer_id, customer=customer)
    return {"customer": db_customer}


@app.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    crud.delete_customer(db=db, customer_id=customer_id)
    return {"message": "Customer deleted"}


@app.post("/{customer_id}/order")
def create_order(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_customer.orders = db_customer.orders + 1
    db_customer = crud.update_customer(db=db, id=customer_id, customer=db_customer)
    return {"customer": db_customer}
