from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import Product,Request
from sqlalchemy import select
from backend.schemas import ProductCreate,ProductUpdate,RequestCreate



async def create_request(db:AsyncSession,request_data:RequestCreate):
    new_request=Request(name=request_data.name,phone=request_data.phone,comment=request_data.comment,product_id=request_data.product_id)
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request


async def get_requests(db:AsyncSession,limit:int=10,skip:int=0):
    query=select(Request).order_by(Request.id.desc()).limit(limit).offset(skip)
    result=await db.execute(query)
    return result.scalars().all()


async def update_request(db:AsyncSession,request_id:int,status:str):
    query=select(Request).where(Request.id == request_id)
    result=await db.execute(query)
    request=result.scalar_one_or_none()
    if request is None:
        return None
    request.status=status.value
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return request