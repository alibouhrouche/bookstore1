import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from . import models, schemas


def get_order(db: Session, order_id: int):
    return db.query(models.Order).options(selectinload(models.Order.order_items)).filter(models.Order.id == order_id).first()


def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_orders_by_owner_id(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.owner_id == owner_id).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        title=order.title,
        status=order.status,
        owner_id=order.owner_id
    )
    db.add(db_order)
    db.flush()
    data = requests.post("http://inventory/items", json=[x.id for x in order.items])
    if data.status_code != 200:
        db.delete(db_order)
        raise HTTPException(status_code=500, detail="Inventory service not available")
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
        db.add(item)
    ret = requests.post("http://customer/" + str(db_order.owner_id) + "/order")
    if ret.status_code != 200:
        raise HTTPException(status_code=500, detail="Customers service not available")
    db.commit()
    db.refresh(db_order)
    return db_order


def add_item_to_order(db: Session, item: schemas.OrderItemCreate, order_id: int):
    db_item = models.OrderItem(
        title=item.title,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
        order_id=order_id,
        item_id=item.item_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db.delete(db_order)
    db.commit()


def update_order(db: Session, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order.id).first()
    db_order.title = order.title
    if db_order.status != order.status:
        if db_order.status == "carted" and order.status != "cancelled":
            requests.post("http://inventory/reserve", json=[{"id": x.item_id, "q": x.quantity} for x in order.items])
        if db_order.status != "carted" and order.status == "cancelled":
            requests.post("http://inventory/release", json=[{"id": x.item_id, "q": x.quantity} for x in order.items])
    db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order
