from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from src.models.orders import Orders
from typing import Optional
from database import get_db

class OrdersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_order(self, title: str, user_id: int):
        query = (
            select(Orders)
            .filter(Orders.title.contains(title), Orders.user_id == user_id)
            )
        res = await self.session.execute(query)
        items = res.scalars().all()
        return items
        
    async def create_order(self, item_id: int):
        query = (
            select(Orders)
            .filter(Orders.id == item_id)
            )
        res = await self.session.execute(query)
        items = res.scalars().all()
        return items

async def get_orders_service(session: AsyncSession = Depends(get_db)):
    return OrdersService(session)
