from fastapi import APIRouter, Depends
from src.servies.user_service import UserService, get_user_service
from src.schemas.users import UserResponse
from src.utils.security import auth

class UserRouter:
    def __init__(self):
        self.router = APIRouter(tags=["User"])
        self._setup_routers()

    def _setup_routers(self):
        self.router.get("/me", response_model=UserResponse)(self.profile)
    
    async def profile(self, 
                      token: str = Depends(auth.access_token_required), 
                      user_service: UserService = Depends(get_user_service)):
        user = await user_service.get_profile(user_id=int(token.sub))
        return user
