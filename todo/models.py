from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


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

    # Relação 1:N - cada usuário pode ter N todos associados a ele.
    todos: Mapped[list['Todo']] = relationship(
        init=False,
        # Quando um usuário for deletado,
        # todos todos associados a ele também serão deletados.
        cascade='all, delete-orphan',
        # Quando fazer um select em User também vai obter os objetos Todo
        # associados a ele.
        lazy='selectin',
    )


@mapped_as_dataclass(table_registry)
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
