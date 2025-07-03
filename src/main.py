from fastapi import FastAPI
from src.create_db import create_db
from src.routers.users import UserRouter
from src.routers.auth import AuthRouter

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_db()

user_router = UserRouter()
auth_router = AuthRouter()

app.include_router(user_router.router)
app.include_router(auth_router.router)