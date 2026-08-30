from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, Integer


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    calorie_target: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    protein_target: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    fat_target: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    carbs_target: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )