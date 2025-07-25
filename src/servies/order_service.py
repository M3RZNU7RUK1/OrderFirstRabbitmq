from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from src.models.orders import Orders
from src.models.items import Items 
from src.database import get_db
from src.models.users import Users 

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
            raise HTTPException(status_code=404, detail="Not found")
        return items
        
    async def create_order(self, item_id: int,user_id: int):
        query = (
            select(Items)
            .filter(Items.id == item_id)
        )
        res = await self.session.execute(query)
        item = res.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        user = await self.session.get(Users, user_id)
        order = Orders(title=item.title , price=item.price, user=user)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order 
    
    async def del_order(self, order_id: int, user_id: int):
        query = (
            select(Orders)
            .filter(Orders.id == order_id, Orders.user_id == user_id)
        )
        res = await self.session.execute(query)
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Not found")
        await self.session.delete(order)
        await self.session.commit()
        
async def get_orders_service(session: AsyncSession = Depends(get_db)):
    return OrdersService(session)
