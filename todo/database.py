from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from todo.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_session() -> AsyncGenerator[AsyncSession]:  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# As alterações feitas aqui somente dizem que a engine agora deve ser
# criada de maneira assíncrona e que a sessão do ORM também será assíncrona.
