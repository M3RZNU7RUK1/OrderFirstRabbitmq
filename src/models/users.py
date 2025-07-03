from src.database import Base, intpk, created_at, updated_at, username_20
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[username_20] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]