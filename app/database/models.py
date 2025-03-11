from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)

    master_password: Mapped[str] = mapped_column(String(61))


class Password(Base):
    __tablename__ = 'passwords'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(String(36))
    hashed_password: Mapped[str] = mapped_column(String(61))
    comment: Mapped[str] = mapped_column(String(), nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
