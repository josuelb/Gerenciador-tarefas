from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    doing = 'doing'
    done = 'done'


@table_registry.mapped_as_dataclass
class UsersModel:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    todos: Mapped[list['TodosModel']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class TodosModel:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    state: Mapped[TodoState]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[UsersModel] = relationship(init=False, back_populates='todos')
