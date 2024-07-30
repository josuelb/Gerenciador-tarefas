from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gnc_todo.database import DB
from gnc_todo.models import UsersModel
from gnc_todo.schemas.schema_user import (
    UserSchema,
    UserSchemaList,
    UserSchemaPublic,
)
from gnc_todo.schemas.schemas_messages import Message
from gnc_todo.security import get_current_user, get_password_hash

router_users = APIRouter(prefix='/users', tags=['users'])
db = DB()
Session_current = Annotated[Session, Depends(db.get_session)]
CurrentUser = Annotated[UsersModel, Depends(get_current_user)]


class Users:

    @router_users.get('/', response_model=UserSchemaList)
    def read_users(session: Session_current, skip: int = 0, limit: int = 100):
        users = session.scalars(
            select(UsersModel).offset(skip).limit(limit)
        ).all()
        return {'users': users}

    @router_users.post(
        '/', status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
    )
    def create_user(session: Session_current, user: UserSchema):
        db_user = session.scalar(
            select(UsersModel).where(
                UsersModel.username == user.username
            )
        )

        if db_user:
            if db_user.username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists'
                )

        hashed_password = get_password_hash(user.password)

        db_user = UsersModel(
            username=user.username,
            password=hashed_password,
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @router_users.put('/{user_id}', response_model=UserSchemaPublic)
    def update_user(
        user_id: int,
        user: UserSchema,
        session: Session_current,
        current_user: CurrentUser
    ):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions',
            )

        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        session.commit()
        session.refresh(current_user)

        return current_user

    @router_users.delete('/{user_id}', response_model=Message)
    def delete_user(
        user_id: int,
        session: Session_current,
        current_user: CurrentUser
    ):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions',
            )

        session.delete(current_user)
        session.commit()

        return {'message': 'User deleted'}
