from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, text
from src.config import settings
import asyncio
from typing import Annotated
from datetime import datetime

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
)

session = async_sessionmaker(engine)

username_20 = Annotated[str, 20]
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]

class Base(DeclarativeBase):    
    type_annotation_map = {
        username_20: String(20)
    }


async def get_db() -> AsyncSession:
    async with session() as sn:
        try:
            yield sn
        except Exception:
            await sn.rollback()
            raise
        finally:
            await sn.close()