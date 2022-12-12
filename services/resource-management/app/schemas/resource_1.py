from pydantic import BaseModel, Field
from typing import Optional


class ResourceBase(BaseModel):
    name:str = Field(title='Название ресурса')
    description: Optional[str] = Field(title='Краткое описание ресурса')
    сount: int = Field(title='Количество ресурса')
    
    class Config:
        orm_mode = True
    
class Resource(ResourceBase):    
    id: int = Field(title='Идентификатор ресурса', default=None)


class ResourceIn(ResourceBase):
    pass