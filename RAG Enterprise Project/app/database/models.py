
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


# ==========================================
# 1. USER MODEL
# ==========================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    username: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50), default="employee", nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    documents: Mapped[list[Document]] = relationship(
        back_populates="uploader"
    )

    conversation: Mapped[Conversation | None] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ==========================================
# 2. DEPARTMENT MODEL
# ==========================================

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    documents: Mapped[list[Document]] = relationship(
        back_populates="department"
    )


# ==========================================
# 3. DOCUMENT MODEL
# ==========================================

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    filename: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500), nullable=False
    )

    file_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50), default="uploaded", nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    department: Mapped[Department] = relationship(
        back_populates="documents"
    )

    uploader: Mapped[User] = relationship(
        back_populates="documents"
    )


# ==========================================
# 4. CONVERSATION MODEL
# ==========================================

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default="Ongoing conversation",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    user: Mapped[User] = relationship(
        back_populates="conversation"
    )

    messages: Mapped[list[Message]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


# ==========================================
# 5. MESSAGE MODEL
# ==========================================

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    conversation: Mapped[Conversation] = relationship(
        back_populates="messages"
    )
