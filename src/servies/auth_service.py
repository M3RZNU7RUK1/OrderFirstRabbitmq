from sqlalchemy.exc import DBAPIError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response, Depends
from src.models.users import Users
from src.utils.security import Security
from src.database import get_db

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.security = Security()

    async def register_user(self, username: str, password: str):
        try:

            existing_user = await self.session.execute(
                select(Users).where(Users.username == username))
            if existing_user.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Username not available")
            
            hashed_password = self.security.hash_password(password)
            user = Users(username=username, password=hashed_password)
            
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            
            return user

        except DBAPIError as e:
            await self.session.rollback()
            if "value too long" in str(e).lower():
                raise HTTPException(status_code=400, detail="Username too long")
            raise HTTPException(status_code=500, detail="Database error")

    async def login_user(self, username: str, password: str, response: Response):
        try:
            result = await self.session.execute(
                select(Users).where(Users.username == username))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            if not self.security.verify_password(user.password, password):
                raise HTTPException(status_code=401, detail="Invalid credentials")
    
            token = self.security.create_jwt(user.id)
            self._set_auth_cookie(response, token)
            
            return {"access_token": token}

        except Exception as e:
            raise HTTPException(status_code=500, detail="Authentication failed")

    def _set_auth_cookie(self, response: Response, token: str):
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=86400, 
            path="/",
        )


async def get_auth_service(session: AsyncSession = Depends(get_db)):
    return AuthService(session)