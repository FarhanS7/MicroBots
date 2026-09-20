"""Integration tests for database ORM models, session isolation, and transaction rollback."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from oap.db import Base, WorkspaceModel, ActorModel, TaskRecordModel


@pytest_asyncio.fixture
async def async_sqlite_session() -> AsyncSession:
    """Isolated in-memory SQLite async session for DB unit/integration tests."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_workspace_model_crud(async_sqlite_session: AsyncSession) -> None:
    ws = WorkspaceModel(id="ws-1", name="Primary Workspace", owner_id="owner-1")
    async_sqlite_session.add(ws)
    await async_sqlite_session.commit()

    result = await async_sqlite_session.execute(select(WorkspaceModel).where(WorkspaceModel.id == "ws-1"))
    fetched = result.scalar_one_or_none()
    assert fetched is not None
    assert fetched.name == "Primary Workspace"
    assert fetched.owner_id == "owner-1"


@pytest.mark.asyncio
async def test_transaction_rollback_does_not_persist(async_sqlite_session: AsyncSession) -> None:
    ws = WorkspaceModel(id="ws-temp", name="Temporary Workspace", owner_id="owner-temp")
    async_sqlite_session.add(ws)
    await async_sqlite_session.rollback()

    result = await async_sqlite_session.execute(select(WorkspaceModel).where(WorkspaceModel.id == "ws-temp"))
    fetched = result.scalar_one_or_none()
    assert fetched is None


@pytest.mark.asyncio
async def test_task_record_model_persistence(async_sqlite_session: AsyncSession) -> None:
    task = TaskRecordModel(id="task-100", workspace_id="ws-1", status="PENDING", payload_json='{"key": "val"}')
    async_sqlite_session.add(task)
    await async_sqlite_session.commit()

    result = await async_sqlite_session.execute(select(TaskRecordModel).where(TaskRecordModel.id == "task-100"))
    fetched = result.scalar_one_or_none()
    assert fetched is not None
    assert fetched.status == "PENDING"
    assert fetched.payload_json == '{"key": "val"}'
