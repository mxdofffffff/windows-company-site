import asyncio
import sys
from fastapi import HTTPException
from backend.database import SessionLocal
from backend.crud.user import get_user_by_username
from backend.models import User
from backend.security import hash_password

async def create_admin(username:str,password:str) -> None:
    async with SessionLocal() as db:
        existing_user = await get_user_by_username(db,username)
        if existing_user:
            raise HTTPException(status_code=400,detail="User already exists")
        user=User(username=username,hashed_passwor=hash_password(password),role="admin")
        db.add(user)
        await db.commit()
        print (f"Админ {username} создан")

if __name__ == "__init__":
    if len(sys.argv) != 3:
        print("Использование: python -m scripts.create_admin <username> <password>")
        sys.exit(1)
    asyncio.run(create_admin(sys.argv[1], sys.argv[2]))

