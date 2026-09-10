from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud
from backend.database import get_db
from backend.schemas import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)

router=APIRouter(prefix="/products",tags=["products"])

@router.get("",response_model=ProductListResponse)
async def get_products(db:AsyncSession=Depends(get_db),limit:int = Query(default=10,ge=1,le=100),skip:int=Query(default=0,ge=0),search:str|None=Query(default=None)):
    items,total=await crud.get_products(db,limit,skip,search)
    return {"data":items,"meta":{"total":total,"limit":limit,"skip":skip}}


@router.get("/{product_id}",response_model=ProductResponse)
async def get_product(product_id:int,db:AsyncSession=Depends(get_db)):
    product=await crud.get_product(db,product_id)
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return product


@router.post("",response_model=ProductResponse)
async def create_product(product:ProductCreate,db:AsyncSession=Depends(get_db)):
    return await crud.create_product(db,product)


@router.patch("/{product_id}",response_model=ProductResponse)
async def update_product(product_id:int,product_data:ProductUpdate,db:AsyncSession=Depends(get_db)):
    product=await crud.update_product(db,product_id,product_data)
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return product


@router.delete("/{product_id}",response_model=ProductResponse)
async def delete_product(product_id:int,db:AsyncSession=Depends(get_db)):
    product = await crud.deactivate_product(db,product_id)
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return product