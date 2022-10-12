from pydantic import BaseModel, Field
from typing import Optional


class Land(BaseModel):
    name:str = Field(title='Название земли')
    description: Optional[str] = Field(title='Краткое описание земли')
    id: int = Field(title='Идентификатор земли')