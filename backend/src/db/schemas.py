from email.policy import default
from typing import Any
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

    # agent mapping
    agents: Mapped[list["Agent"]] = relationship("Agent", back_populates="user", cascade="all, delete-orphan")

    def to_safe_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Agent(Base):
    __tablename__ = "Agents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Agent Card Fields
    protocolVersion: Mapped[str] = mapped_column(String(10), default="0.3.0")
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), default="http://agenthub.com/a2a")
    version: Mapped[str] = mapped_column(String(255), default="0.1")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key + relationship
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="agents")

