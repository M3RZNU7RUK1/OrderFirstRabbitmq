from src.database import Base, intpk, created_at, updated_at
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[intpk] 
    title: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["Users"] = relationship(
        back_populates="orders"
    )
