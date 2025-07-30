from src.database import Base, intpk, created_at, updated_at, username_20
from sqlalchemy.orm import Mapped, mapped_column, relationship 

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[username_20]
    password: Mapped[str]
    phone_number: Mapped[str]
    role: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=True)

    orders: Mapped[list["Orders"]] = relationship(
        back_populates="user",
        lazy="selectin"
    )

    
