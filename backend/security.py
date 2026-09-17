from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from pathlib import Path
from jose import jwt,JWTError
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent / ".env")

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data:dict, expires_delta:timedelta|None=None):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token:str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None