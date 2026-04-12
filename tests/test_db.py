from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo.models import User


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

    new_user_dict = asdict(new_user)
    new_user_dict.update({'id': 1})
    new_user_dict.update({'created_at': time})  # time gerado por mock_db_time
    new_user_dict.update({'updated_at': time})

    assert user is not None
    assert asdict(user) == new_user_dict
