from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from src.models.items import Items
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
    
    async def add_item(self, title: str, description: str, price: int):
        item = Items(title=title, description=description, price=price)

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item
    async def del_item(self, item_id: int):
        query = (
            select(Items)
            .filter(Items.id == item_id)
        )
        res = await self.session.execute(query)
        item = res.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Нету такого :)")
        await self.session.delete(item)
        await self.session.commit()
async def get_items_service(session: AsyncSession = Depends(get_db)):
    return ItemsService(session)
