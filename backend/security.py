from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from pathlib import Path
from jose import jwt,JWTError
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent / ".env")

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire, "type":"access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire, "type":"refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token:str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None