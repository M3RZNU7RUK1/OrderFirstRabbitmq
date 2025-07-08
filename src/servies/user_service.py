from src.models.users import Users
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, Depends
from src.database import get_db
from src.utils.security import Security
from dotenv import load_dotenv
import os

load_dotenv()

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.security = Security()

    async def get_profile(self, user_id: int):
        try:
            query = (
                select(Users)
                .filter(Users.id == user_id)
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

    async def add_admin(self):
        admin = Users(username=os.getenv("USERNAME_ADMIN"), 
                      password=self.security.hash_password(os.getenv("PASSWORD_ADMIN")),
                      role="admin")
        self.session.add(admin)
        await self.session.commit()
        
async def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)
