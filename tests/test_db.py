from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo.models import Todo, User


@pytest.mark.asyncio  # diz ao pytest que esse test contém código assíncrono
async def test_create_user(session: AsyncSession, mock_db_time):  # type: ignore
    with mock_db_time(model=User) as time:  # type: ignore
        new_user = User(
            username='Alice', email='alice@example.com', password='secret'
        )

        session.add(new_user)
        await session.commit()  # categorizado como operação I/O

    # categorizado como operação I/O (input/output)
    user = await session.scalar(select(User).where(User.username == 'Alice'))

    assert user is not None
    assert asdict(user) == {
        'id': 1,
        'username': 'Alice',
        'email': 'alice@example.com',
        'password': 'secret',
        'created_at': time,  # time gerado por mock_db_time
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session: AsyncSession, user: User, mock_db_time):
    with mock_db_time(model=Todo) as time:
        todo = Todo(
            title='Test Todo',
            description='Test Desc',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()

        todo = await session.scalar(select(Todo))

        assert todo is not None
        assert asdict(todo) == {
            'description': 'Test Desc',
            'id': 1,
            'state': 'draft',
            'title': 'Test Todo',
            'user_id': 1,
            'created_at': time,
            'updated_at': time,
        }


@pytest.mark.asyncio
async def test_user_todo_relationship(session: AsyncSession, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    db_user = await session.scalar(select(User).where(User.id == user.id))

    assert db_user is not None
    assert db_user.todos == [todo]
