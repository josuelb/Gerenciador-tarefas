from pydantic import BaseModel

from gnc_todo.models import TodoState


class TodoSchema(BaseModel):
    id:int
    title: str
    description: str
    state: TodoState


class TodoSchemaPublic(BaseModel):
    id: int


class TodoSchemaList(BaseModel):
    todos: list[TodoSchemaPublic]


class TodoSchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
