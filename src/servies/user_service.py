from src.models.users import Users
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, Depends
from database import get_db

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_profile(self, user_id: str):
        try:
            query = (
                select(Users)
                .where(Users.id == int(user_id))
                .options(selectinload(Users.posts))
            )
            
            res = await self.session.execute(query)
            user = res.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
                
            return user
            
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
async def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)