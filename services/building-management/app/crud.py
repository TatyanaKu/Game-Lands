import typing
from sqlalchemy.orm import Session
from .database import models
from . import schemas

def create_building(
        db: Session, building: schemas.BuildingIn
    ) -> models.Building:
    '''
    Создает
    '''
    db_building = models.Building(
        name = building.name,
        description = building.description,
        level = building.level,
        type = building.type,
        landID = building.landID
    )
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

def get_buildings(
        db: Session, skip: int = 0, limit: int = 100
    ) -> typing.List[models.Building]:
    '''
    Возвращает информацию
    '''
    return  db.query(models.Building) \
            .offset(skip) \
            .limit(limit) \
            .all()

def get_building(
        db: Session, building_id: int
    ) -> models.Building:
    '''
    Возвращает информацию о конкретной
    '''
    return  db.query(models.Building) \
            .filter(models.Building.id == building_id) \
            .first()

def update_building(
        db: Session, building_id: int, building: schemas.BuildingIn
    ) -> models.Building:
    '''
    Обновляет информацию
    '''
    result =    db.query(models.Building) \
                .filter(models.Building.id == building_id) \
                .update(building.dict())
    db.commit()

    if result == 1:
        return get_building(db, building_id)
    return None


def delete_building(
        db: Session, building_id: int
    ) -> bool:
    result =    db.query(models.Building) \
                .filter(models.Building.id == building_id) \
                .delete()
    db.commit()
    return result == 1