from sqlalchemy.orm import Session

from . import models, schemas
from .schemas import ItemCatch


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def search_items(db: Session, query: str):
    return db.query(models.Item).filter(models.Item.title.contains(query)).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item.id).first()
    db_item.title = item.title
    db_item.description = item.description
    db_item.price = item.price
    db_item.stock = item.stock
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()


def reserve_items(db: Session, items: list[ItemCatch]):
    for x in items:
        db_item = db.query(models.Item).filter(models.Item.id == x.id).first()
        if db_item.stock < x.q:
            raise Exception("Not enough items in stock")
        db_item.stock -= x.q
    db.commit()
    return {"message": "Items captured"}


def release_items(db: Session, items: list[ItemCatch]):
    for x in items:
        db_item = db.query(models.Item).filter(models.Item.id == x.id).first()
        db_item.stock += x.q
    db.commit()
    return {"message": "Items released"}
