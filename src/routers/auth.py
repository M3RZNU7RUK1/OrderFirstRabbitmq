from fastapi import APIRouter, Response, Depends
from src.servies.auth_service import AuthService, get_auth_service

class AuthRouter:
    def __init__(self):
        self.router = APIRouter(tags=["Auth"])
        self._setup_routers()

    def _setup_routers(self):
        self.router.post("/register")(self.register_user)
        self.router.post("/login")(self.login_user)
    
    async def register_user(self, username: str, password: str, phone_number: str,auth_service: AuthService = Depends(get_auth_service)):
        user = await auth_service.register_user(username=username, password=password, phone_number=phone_number)
        return user

    async def login_user(self, username: str, password: str, phone_number: str, response: Response, auth_service: AuthService = Depends(get_auth_service)):
        token = await auth_service.login_user(username=username, password=password, response=response, phone_number=phone_number)
        return token
