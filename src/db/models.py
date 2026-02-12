import uuid
from datetime import date as db_date
from sqlalchemy import String, BigInteger, ForeignKey, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    role: Mapped[str] = mapped_column(String(20), default="user")

    settings: Mapped["UserSettings"] = relationship(back_populates="user", uselist=False, cascade="all, delete")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="user", cascade="all, delete")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    currency: Mapped[str] = mapped_column(String(10), default="RUB")
    daily_limit: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="settings")


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    amount: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str | None] = mapped_column(String(255))
    date: Mapped[db_date] = mapped_column(Date)

    user: Mapped["User"] = relationship(back_populates="expenses")
