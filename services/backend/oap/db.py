"""Database session and SQLAlchemy ORM baseline models."""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Text, Boolean


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/microbots",
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""
    pass


class WorkspaceModel(Base):
    """Workspace entity model."""
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ActorModel(Base):
    """Actor identity model."""
    __tablename__ = "actors"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class TaskRecordModel(Base):
    """Durable task record model."""
    __tablename__ = "task_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


def get_engine(url: str | None = None) -> AsyncEngine:
    """Create async engine for PostgreSQL connection."""
    target_url = url or DATABASE_URL
    # SQLite async fallback for tests if postgresql is unavailable
    if target_url.startswith("sqlite"):
        return create_async_engine(target_url, echo=False)
    return create_async_engine(target_url, echo=False, pool_pre_ping=True)


def get_session_factory(engine: AsyncEngine | None = None) -> async_sessionmaker[AsyncSession]:
    """Get session factory for async sessions."""
    eng = engine or get_engine()
    return async_sessionmaker(eng, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding database sessions."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session
