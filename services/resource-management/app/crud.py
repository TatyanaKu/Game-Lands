import typing
from sqlalchemy.orm import Session
from .database import models
from . import schemas

def create_resource(
        db: Session, resource: schemas.ResourceIn
    ) -> models.Resource:
    '''
    Создает
    '''
    db_resource = models.Resource(
        name = resource.name,
        description = resource.description,
        сount = resource.сount
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def get_resources(
        db: Session, skip: int = 0, limit: int = 100
    ) -> typing.List[models.Resource]:
    '''
    Возвращает информацию
    '''
    return  db.query(models.Resource) \
            .offset(skip) \
            .limit(limit) \
            .all()

def get_resource(
        db: Session, resource_id: int
    ) -> models.Resource:
    '''
    Возвращает информацию о конкретном
    '''
    return  db.query(models.Resource) \
            .filter(models.Resource.id == resource_id) \
            .first()

def update_resource(
        db: Session, resource_id: int, resource: schemas.ResourceIn
    ) -> models.Resource:
    '''
    Обновляет информацию
    '''
    result =    db.query(models.Resource) \
                .filter(models.Resource.id == resource_id) \
                .update(resource.dict())
    db.commit()

    if result == 1:
        return get_resource(db, resource_id)
    return None


def delete_resource(
        db: Session, resource_id: int
    ) -> bool:
    result =    db.query(models.Resource) \
                .filter(models.Resource.id == resource_id) \
                .delete()
    db.commit()
    return result == 1