from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from todo.app import app
from todo.database import get_session
from todo.models import User, table_registry


@pytest.fixture
def client(session: Session) -> Generator[TestClient]:
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session() -> Generator[Session]:
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)  # elimina todas as tabelas
    engine.dispose()  # fecha a conexão com o banco de dados


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


@pytest.fixture
def user(session: Session) -> User:
    user = User(username='Test', email='test@test.com', password='test_secret')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
