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

    async def register_user(self, username: str, password: str, phone_number: str):
        existing_user = await self.session.execute(
            select(Users).filter(Users.username == username))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Username not available")
            
        hashed_password = self.security.hash_password(password)
        user = Users(username=username, 
                    password=hashed_password, 
                    phone_number=str(self.security.encrypt(data=phone_number)),
                    role="user")
   
        self.session.add(user)
        await self.session.commit()
        return "Okey!"

    async def login_user(self, username: str, password: str, phone_number: str, response: Response):
        query = (
            select(Users)
            .filter(Users.username == username)
        )
        res = await self.session.execute(query)
        user = res.scalar_one_or_none()
        is_valid = bool(user) and self.security.verify_password(user.password, password)
        if not is_valid:
            if not user:
                self.security.verify_password(hashed_pwd=user.password, password=password)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if self.security.decrypt(token=user.phone_number[2:-1].encode()) != phone_number:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = self.security.create_jwt(user_id=user.id, user_role=user.role)
        self._set_auth_cookie(response, token)
            
        return {"access_token": token}


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
