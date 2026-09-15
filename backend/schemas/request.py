from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import re
from enum import Enum

PHONE_PATTERN=re.compile(r"^(\+7|8)\d{10}$")

class RequestCreate(BaseModel):
    name:str = Field(min_length=1, max_length=50)
    phone:str
    comment:str|None=None
    product_id:int|None=None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls,value:str):
        cleaned=value.replace(" ","").replace("-","")
        if not PHONE_PATTERN.match(cleaned):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
        return cleaned


class RequestResponse(BaseModel):
    id:int
    name:str
    phone:str
    comment:str|None
    product_id:int|None
    status:str
    created_at:datetime

    class Config:
        from_attributes = True


class RequestStatus(str,Enum):
    NEW="Новый заказ"
    IN_PROGRESS="Выполняется"
    DONE="Выполнено"
    CANCELED="Отменено"


class RequestUpdate(BaseModel):
    status:RequestStatus