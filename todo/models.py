from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    # Mapped refere-se a um atributo Python que é associado (ou mapeado)
    # a uma coluna especifica em uma tabela de banco de dados.

    # init=False diz que o parâmetro id não deve ser passado.
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
