from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from src.models.items import Items
from typing import Optional
from src.database import get_db

class ItemsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_items(self, title: str):
        query = (
            select(Items)
            .filter(Items.title.contains(title))
            )
        res = await self.session.execute(query)
        items = res.scalars().all()
        return items

async def get_items_service(session: AsyncSession = Depends(get_db)):
    return ItemsService(session)