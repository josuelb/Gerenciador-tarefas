from sqlalchemy import select

from gnc_todo.models import TodosModel, UsersModel


def test_create_user(session):
    new_user = UsersModel(username='alice', password='secret')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(UsersModel).where(UsersModel.username == 'alice'))

    assert user.username == 'alice'


def test_create_todo(session, user: UsersModel):
    todo = TodosModel(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(UsersModel).where(UsersModel.id == user.id))

    assert todo in user.todos