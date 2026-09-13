from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
import re

PHONE_PATTERN=re.compile(r"^(\+7|8)\d{10}$")


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0)

class ProductUpdate(BaseModel):
    name: str| None = Field(default=None,min_length=1, max_length=100)
    description: str| None = Field(default=None,min_length=1, max_length=100)
    price: Decimal| None = Field(default=None,gt=0)
    is_active: bool| None = None

class ProductResponseImage(BaseModel):
    id: int
    filepath: str
    sort_order: int

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    is_active: bool
    images: list[ProductResponseImage] = []

    class Config:
        from_attributes = True

class Meta(BaseModel):
    total:int
    limit:int
    skip:int

class ProductListResponse(BaseModel):
    data: list[ProductResponse]
    meta: Meta


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