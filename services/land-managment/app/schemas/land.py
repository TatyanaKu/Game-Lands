from pydantic import BaseModel, Field
from typing import Optional


class LandBase(BaseModel):
    name:str = Field(title='Название земли')
    description: Optional[str] = Field(title='Краткое описание земли')
    ieee_address: str = Field(title='IEEEE-адрес земли')

class Land(LandBase):
    id: int = Field(title='Идентификатор земли')
    info: dict = Field(title='Информация о земле')