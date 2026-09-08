from sqlalchemy.ext.asyncio import AsyncSession
from models import Product
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload
from schemas import ProductCreate,ProductUpdate

async def get_products(db:AsyncSession,limit:int=10,skip:int=0,search:str|None = None,only_active:bool=True):
    query=select(Product).options(selectinload(Product.images))
    if only_active:
        query=query.where(Product.is_active==True)
    if search:
        query=query.where(Product.name.ilike(f"%{search}%"))
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query).scalar_one())
    query = query.order_by(Product.id.desc()).limit(limit).offset(skip)
    items = (await db.execute(query).scalars().all())
    return items,total


async def get_product(db:AsyncSession,product_id:int):
    query=select(Product).options(selectinload(Product.images)).where(Product.id == product_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_product(db:AsyncSession,product:ProductCreate):
    new_product=Product(name=product.name,description=product.description,price=product.price)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def update_product(db:AsyncSession,product_id:int,product_data:ProductUpdate):
    product = await get_product(db,product_id)
    if product is None:
        return None
    update_fields = product_data.model_dump(exclude_unset=True)
    for field,value in update_fields.items():
        setattr(product,field,value)
    await db.commit()
    await db.refresh(product)
    return product


async def deactivate_product(db:AsyncSession,product_id:int):
    product=await get_product(db,product_id)
    if product is None:
        return None
    product.is_active=False
    await db.commit()
    return product