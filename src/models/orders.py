from src.database import Base, intpk, created_at, updated_at
from sqlalchemy.orm import Mapped, relationship  

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[intpk]
    title: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    user: Mapped["Users"] = relationship(
        back_populates="orders"
    )
