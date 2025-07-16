from src.database import Base, engine
from src.models.items import Items
from src.models.orders import Orders
from src.models.users  import Users

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(
            bind=sync_conn,
            tables=[
                Items.__table__,
                Orders.__table__,
                Users.__table__
            ]
        ))
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
