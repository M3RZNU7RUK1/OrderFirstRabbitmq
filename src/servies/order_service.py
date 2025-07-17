from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from src.models.orders import Orders
from src.models.items import Items 
from src.database import get_db
import random 
from src.schemas.orders import OrderResponse

class OrdersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_order(self, title: str, user_id: int):
        query = (
            select(Orders)
            .filter(Orders.title == title, Orders.user_id == user_id)
            )
        res = await self.session.execute(query)
        items = res.scalars().all()
        if items == []:
            raise HTTPException(status_code=404, detail="Нету такого :)")
        return items
        
    async def create_order(self, item_id: int, user_id: int):
        query = (
            select(Items)
            .filter(Items.id == item_id)
        )
        res = await self.session.execute(query)
        item = res.scalar_one_or_none() 
        if not item:
            raise HTTPException(status_code=404, detail="Нету такого :)")
        delivery_time = f"Заказ будет доставлен в: {random.randint(1, 12)}:{random.randint(0, 59):02d}{random.choice(['am', 'pm'])}"
        order = Orders(title=item.title, description=delivery_time, price=item.price, user_id=user_id)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return OrderResponse(
            id=order.id,
            title=order.title,
            description=order.description,
            price=order.price,
            user_id=order.user_id,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
    
    async def del_order(self, order_id: int, user_id: int):
        query = (
            select(Orders)
            .filter(Orders.id == order_id, Orders.user_id == user_id)
        )
        res = await self.session.execute(query)
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Нету такого :)")
        await self.session.delete(order)
        await self.session.commit()
        
async def get_orders_service(session: AsyncSession = Depends(get_db)):
    return OrdersService(session)
