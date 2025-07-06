from src.database import Base, intpk, created_at, updated_at
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint

class Items(Base):
    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint("price >= 1", name="check_price_positive"),
    )

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
