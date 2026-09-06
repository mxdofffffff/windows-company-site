from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)

class ProductUpdate(BaseModel):
    name: str| None = Field(default=None,min_length=1, max_length=100)
    description: str| None = Field(default=None,min_length=1, max_length=100)
    price: float| None = Field(default=None,gt=0)
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
    price: float
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