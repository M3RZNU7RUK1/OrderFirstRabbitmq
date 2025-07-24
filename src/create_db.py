from src.database import Base, engine

async def create_db():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
    print("ready")
