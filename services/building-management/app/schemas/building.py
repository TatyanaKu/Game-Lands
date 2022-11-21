from pydantic import BaseModel, Field
from typing import Optional


class BuildingBase(BaseModel):
    name:str = Field(title='Название постройки')
    description: Optional[str] = Field(title='Краткое описание постройки')
    level: int = Field(title='Уровень постройки')
    type: Optional[str] = Field(title='Тип постройки')
    landid: Optional[int] = Field(title='Идентификатор земли на которой расположена постройка')
    
    class Config:
        orm_mode = True
    
class Building(BuildingBase):    
    id: int = Field(title='Идентификатор постройки', default=None)



class BuildingIn(BuildingBase):
    pass
