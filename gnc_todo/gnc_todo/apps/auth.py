from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from gnc_todo.database import DB
from gnc_todo.models import UsersModel
from gnc_todo.schemas.schemas_auth import TokenSchema
from gnc_todo.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router_auth = APIRouter(prefix='/auth', tags=['auth'])
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
db = DB()
Session_current = Annotated[Session, Depends(db.get_session)]

class Auth:

    @router_auth.post('/token', response_model=TokenSchema)
    def login_for_access_token(session: Session_current,
        form_data: OAuth2Form
    ):
        user = session.scalar(
            select(UsersModel).where(
                UsersModel.username == form_data.username
            )
        )

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect email or password',
            )

        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect email or password',
            )

        access_token = create_access_token(data={'sub': user.username})

        return {'access_token': access_token, 'token_type': 'bearer'}

    @router_auth.post('/refresh_token', response_model=TokenSchema)
    def refresh_access_token(
        user: UsersModel = Depends(get_current_user)
    ):
        new_access_token = create_access_token(data={'sub': user.username})

        return {'access_token': new_access_token, 'token_type': 'bearer'}
