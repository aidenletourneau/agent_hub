from sqlalchemy import (
    String, DateTime, Boolean, ForeignKey, Index, func, UniqueConstraint, Text
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from sqlalchemy.types import Uuid

from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
import hashlib


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    __table_args__ = (
        UniqueConstraint("google_sub", name="uq_user_google_sub"),
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint("email", name="uq_user_email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str | None] = mapped_column(String(40))
    password_hash: Mapped[str | None] = mapped_column(Text())      # only for local users
    google_sub: Mapped[str] = mapped_column(String(255), nullable=True)   # OIDC 'sub'
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    name: Mapped[str | None] = mapped_column(String(200))
    image_url: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



# def utcnow() -> datetime:
#     return datetime.now(timezone.utc)

# def expires_in_15m() -> datetime:
#     return datetime.now(timezone.utc) + timedelta(minutes=3)


# class Session(Base):
#     __tablename__ = "Sessions"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, server_default=func.now())
#     expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=expires_in_15m)


#     def is_expired(self) -> bool:
#         return utcnow() >= self.expires_at
