from contextlib import contextmanager
from datetime import datetime
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from todo.app import app
from todo.database import get_session
from todo.models import User, table_registry
from todo.security import get_password_hash


@pytest.fixture
def client(session: Session) -> Generator[TestClient]:
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # engine.begin() inicia um transação assíncrona com o banco de dados
    async with engine.begin() as conn:
        # inicia a criação de tabelas, uma operação síncrona por natureza
        # Esse processo assegura que a criação das tabelas ocorra de forma
        # não bloqueante.
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        # elimina todas as tabelas
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@contextmanager
def _mock_db_time(*, model: Any, time: datetime = datetime(2024, 1, 1)):

    # Função para alterar o atributo created_at do objeto target
    def fake_time_hook(mapper, connection, target: Any):  # type: ignore
        if hasattr(target, 'created_at'):
            target.created_at = time

        if hasattr(target, 'updated_at'):
            target.updated_at = time

    # Adiciona um evento a um model.
    # Executa uma função (Hook)antes de inserir o registro no bando de dados.
    event.listen(model, 'before_insert', fake_time_hook)  # type: ignore

    yield time  # retorna o datetime na abertura do gerenciamento de contexto

    event.remove(model, 'before_insert', fake_time_hook)  # type: ignore


@pytest_asyncio.fixture
async def user(session: AsyncSession) -> User:
    plain_password = 'test_secret'

    user = User(
        username='Test',
        email='test@test.com',
        password=get_password_hash(plain_password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
def token(client: TestClient, user: User) -> str:
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': 'test_secret'}
    )

    return response.json()['access_token']
