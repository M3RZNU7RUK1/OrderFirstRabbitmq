from src.database import Base, intpk, created_at, updated_at
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship(
        "Users",
        back_populates="orders",
    )