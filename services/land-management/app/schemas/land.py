from pydantic import BaseModel, Field
from typing import Optional


class LandBase(BaseModel):
    name:str = Field(title='Название земли')
    description: Optional[str] = Field(title='Краткое описание земли')
    
    class Config:
        orm_mode = True
    
class Land(LandBase):    
    id: int = Field(title='Идентификатор земли', default=None)


class LandIn(LandBase):
    pass