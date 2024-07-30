from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gnc_todo.settings import Settings

engine = create_engine(Settings().DATABASE_URI)


class DB:
    @staticmethod
    def get_session():
        with Session(engine) as session:
            yield session
