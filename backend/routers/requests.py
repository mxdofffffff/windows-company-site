from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import RequestResponse,RequestCreate,RequestUpdate
from backend.models import *
from fastapi import Depends,APIRouter,Query,HTTPException
from backend.database import get_db
from backend import crud

request_router = APIRouter(prefix="/requests",tags=["requests"])

@request_router.post("",response_model=RequestResponse)
async def create_request(request:RequestCreate,db:AsyncSession=Depends(get_db)):
    return await crud.create_request(db,request)

@request_router.get("",response_model=list[RequestResponse])
async def get_requests(db:AsyncSession=Depends(get_db),limit:int=Query(default=10,ge=1,le=100),skip:int=Query(default=0,ge=0)):
    return await crud.get_requests(db,limit,skip)

@request_router.patch("/{request_id}", response_model=RequestResponse)
async def update_request(request_id: int, data: RequestUpdate, db: AsyncSession = Depends(get_db)):
    request = await crud.update_request_status(db, request_id, data.status)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request