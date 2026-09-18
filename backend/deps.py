from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.security import decode_access_token
from backend.crud import user as crud
from backend.models import User

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str = Depends(oauth2_scheme),db:AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"})
    payload=decode_access_token(token)
    if not payload:
        raise credentials_exception
    username:str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = await crud.get_user_by_username(db,username)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user:User = Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,details="Not enough permissions")
    return current_user
