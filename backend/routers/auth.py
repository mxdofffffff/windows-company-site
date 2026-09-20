from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException,status
from backend.schemas.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.crud import user as crud
from backend.security import verify_password, create_access_token
auth_router=APIRouter(prefix="/auth",tags=["auth"])


@auth_router.post("/login",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession=Depends(get_db)):
    user = await crud.get_user_by_username(db,form_data.username)
    if user is None or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"},)
    access_token=create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"bearer"}