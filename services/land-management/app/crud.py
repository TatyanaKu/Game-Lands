import typing
from sqlalchemy.orm import Session
from .database import models
from . import schemas

def create_land(
        db: Session, land: schemas.LandIn
    ) -> models.Land:
    '''
    Создает
    '''
    db_land = models.Land(
        name = land.name,
        description = land.description
    )
    db.add(db_land)
    db.commit()
    db.refresh(db_land)
    return db_land

def get_lands(
        db: Session, skip: int = 0, limit: int = 10
    ) -> typing.List[models.Land]:
    '''
    Возвращает информацию
    '''
    return  db.query(models.Land) \
            .offset(skip) \
            .limit(limit) \
            .all()

def get_land(
        db: Session, land_id: int
    ) -> models.Land:
    '''
    Возвращает информацию о конкретной
    '''
    return  db.query(models.Land) \
            .filter(models.Land.id == land_id) \
            .first()

def update_land(
        db: Session, land_id: int, land: schemas.LandIn
    ) -> models.Land:
    '''
    Обновляет информацию
    '''
    result =    db.query(models.Land) \
                .filter(models.Land.id == land_id) \
                .update(land.dict())
    db.commit()

    if result == 1:
        return get_land(db, land_id)
    return None


def delete_land(
        db: Session, land_id: int
    ) -> bool:
    result =    db.query(models.Land) \
                .filter(models.Land.id == land_id) \
                .delete()
    db.commit()
    return result == 1