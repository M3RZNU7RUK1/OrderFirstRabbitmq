from fastapi import FastAPI
from src.create_db import create_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_db()