from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_redis_cache import cache
from sqlalchemy import select
from sqlalchemy.orm import Session

from gnc_todo.database import DB
from gnc_todo.models import TodosModel, UsersModel
from gnc_todo.schemas.schemas_messages import Message
from gnc_todo.schemas.schemas_todo import (
    TodoSchema,
    TodoSchemaList,
    TodoSchemaPublic,
    TodoSchemaUpdate,
)
from gnc_todo.security import get_current_user

router_todo = APIRouter(prefix='/todo', tags=["todo"])
db = DB()
Session_current = Annotated[Session, Depends(db.get_session)]
CurrentUser = Annotated[UsersModel, Depends(get_current_user)]


class Todo:
    @cache()
    @router_todo.post('/', response_model=TodoSchema)
    def create_todo(
        todo: TodoSchema,
        session: Session_current,
        user: CurrentUser
    ):
        db_todo: TodosModel = TodosModel(
            title=todo.title,
            description=todo.description,
            state=todo.state,
            user_id=user.id,
        )
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return db_todo

    @router_todo.get('/', response_model=TodoSchemaList)
    def list_todos(  # noqa
        user: CurrentUser,
        session: Session_current,
        title: str = Query(None),
        description: str = Query(None),
        state: str = Query(None),
        offset: int = Query(None),
        limit: int = Query(None),
    ):

        query = select(TodosModel).where(TodosModel.user_id == user.id)

        if title:
            query = query.filter(TodosModel.title.contains(title))

        if description:
            query = query.filter(TodosModel.description.contains(description))

        if state:
            query = query.filter(TodosModel.state == state)

        todos = session.scalars(query.offset(offset).limit(limit)).all()

        return {'todos': todos}
    
    @cache()
    @router_todo.patch('/{todo_id}', response_model=TodoSchema)
    def patch_todo(
        todo_id: int,
        user: CurrentUser,
        session: Session_current,
        todo: TodoSchemaUpdate,
    ):
        db_todo = session.scalar(
            select(TodosModel).where(
                TodosModel.user_id == user.id, TodosModel.id == todo_id
            )
        )

        if not db_todo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
            )

        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)

        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return db_todo

    @router_todo.delete('/{todo_id}', response_model=Message)
    def delete_todo(todo_id: int, session: Session_current, user: CurrentUser):
        todo = session.scalar(
            select(TodosModel).where(
                TodosModel.user_id == user.id, TodosModel.id == todo_id
            )
        )

        if not todo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
            )

        session.delete(todo)
        session.commit()

        return {'message': 'Task has been deleted successfully.'}
