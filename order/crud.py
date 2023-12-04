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
        owner_id=order.owner_id,
    )
    db.add(db_order)
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
