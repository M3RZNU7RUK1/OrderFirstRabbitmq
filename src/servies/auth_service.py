from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response, Depends
from src.models.users import Users
from src.utils.security import Security, auth 
from src.database import get_db

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.security = Security()

    async def register_user(self, username: str, password: str, phone_number: str):
        query = (
            select(Users)
            .filter(Users.username == username)
        )
        res = await self.session.execute(query)
        user = res.scalar_one_or_none()
        if user:
            raise HTTPException(status_code=409, detail="Username not avaible")
        hashed_password = self.security.hash(password)
        user = Users(username=username, 
                    password=hashed_password, 
                    phone_number=str(self.security.encrypt(data=phone_number)),
                    role="user")
   
        self.session.add(user)
        await self.session.commit()
        return "Successfully"

    async def login_user(self, username: str, password: str, phone_number: str, response: Response):
        query = (
            select(Users)
            .filter(Users.username == username)
        )
        res = await self.session.execute(query)
        user = res.scalar_one_or_none()
        is_valid = bool(user) and self.security.verify(user.password, password)
        if not is_valid:
            if not user:
                self.security.verify(user.password, password)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if self.security.decrypt(token=user.phone_number[2:-1].encode()) != phone_number:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token, refresh_token = self.security.create_jwt(user_id=user.id, user_role=user.role)
        user.refresh_token = self.security.hash(refresh_token)
        user.is_active = True
        self._set_auth_cookie(response, access_token)
                
        return {"access_token": access_token,
                "refresh_token": refresh_token
                }
    
    async def refresh_access_token(self, refresh_token: str, response: Response):
        try:
            payload = auth.verify_token(refresh_token)
            user_id = int(payload.sub)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        query = (
            select(Users).
            filter(Users.id == user_id)
        )
        res = await self.session.execute(query)
        user = res.scalar_one_or_none()
        
        if not user or not user.refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        if not self.security.verify(user.refresh_token, refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        new_access_token, new_refresh_token = self.security.create_jwt(
            user_id=user.id, 
            user_role=user.role
        )
        
        user.refresh_token = self.security.hash(new_refresh_token)
        await self.session.commit()
        
        self._set_auth_cookie(response, new_access_token)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token  
        }


    async def logout(self, user_id: int, response: Response):
        user = await self.session.get(Users, user_id)
        if user:
            user.refresh_token = None
            user.is_active = False
            await self.session.commit()
        
        response.delete_cookie("access_token")
        return {"message": "Successfully logged out"}

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
