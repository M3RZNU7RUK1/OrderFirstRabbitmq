from fastapi import FastAPI 
from src.create_db import create_db
from src.routers.users import UserRouter
from src.routers.auth import AuthRouter
from src.routers.items import ItemRouter
from src.routers.orders import OrderRourer 
from src.servies.user_service import UserService  
from contextlib import asynccontextmanager 
from src.database import session 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    async with session() as sn:
        user_service = UserService(sn)
        await user_service.add_admin()
    
    yield
app = FastAPI(lifespan=lifespan)
user_router = UserRouter()
auth_router = AuthRouter()
item_router = ItemRouter()
order_router = OrderRourer()

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(item_router.router)
app.include_router(order_router.router)
