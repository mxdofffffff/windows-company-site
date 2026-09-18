from backend.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_user_by_username(db:AsyncSession, username:User):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()