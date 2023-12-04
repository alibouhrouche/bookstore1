from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .schemas import ItemCatch

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
    items = crud.get_items(db, skip=skip, limit=limit)
    return {"items": items}


@app.post("/")
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db=db, item=item)
    return {"item": db_item}


@app.get("/search")
def search_items(query: str, db: Session = Depends(get_db)):
    items = crud.search_items(db=db, query=query)
    return {"items": items}


@app.get("/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": db_item}


@app.get("/{item_id}/stock")
def read_item_stock(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"stock": db_item.stock}


@app.patch("/{item_id}")
@app.put("/{item_id}")
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.id = db_item.id
    item.title = db_item.title if item.title is None else item.title
    item.description = db_item.description if item.description is None else item.description
    item.price = db_item.price if item.price is None else item.price
    item.stock = db_item.stock if item.stock is None else item.stock
    db_item = crud.update_item(db=db, item=item)
    return {"item": db_item}


@app.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db=db, item_id=item_id)
    return {"message": "Item deleted"}


@app.post("/items")
def get_items(v: list[int], db: Session = Depends(get_db)):
    ret = {}
    for i in v:
        ret[i] = crud.get_item(db=db, item_id=i)
    return {"items": ret}


@app.post("/reserve")
def reserve_items(v: list[ItemCatch], db: Session = Depends(get_db)):
    return crud.reserve_items(db=db, items=v)


@app.post("/release")
def release_items(v: list[ItemCatch], db: Session = Depends(get_db)):
    return crud.release_items(db=db, items=v)
