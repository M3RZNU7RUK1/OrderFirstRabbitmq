from fastapi import APIRouter, HTTPException, Response, Depends, Request
from src.servies.auth_service import AuthService, get_auth_service
from src.schemas.users import UserRegister

class AuthRouter:
    def __init__(self):
        self.router = APIRouter(tags=["Auth"], prefix="/auth")
        self._setup_routers()

    def _setup_routers(self):
        self.router.post("/register")(self.register_user)
        self.router.post("/login")(self.login_user)
        self.router.post("/refresh")(self.refresh_token)

    async def refresh_token(
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
    ):
        data = await request.json()
        refresh_token = data.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token required")
        
        return await auth_service.refresh_access_token(refresh_token, response)   

    async def logout(user_id: int, response: Response, auth_service: AuthService = Depends(get_auth_service)):
        return await auth_service.logout(user_id, response)

    async def register_user(self, user_data: UserRegister, auth_service: AuthService = Depends(get_auth_service)):
        user = await auth_service.register_user(username=user_data.username, password=user_data.password, phone_number=user_data.phone_number)
        return user

    async def login_user(self,  user_data: UserRegister, response: Response, auth_service: AuthService = Depends(get_auth_service)):
        token = await auth_service.login_user(username=user_data.username, password=user_data.password, response=response, phone_number=user_data.phone_number)
        return token
