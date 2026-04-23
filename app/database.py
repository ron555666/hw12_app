import os
from sqlmodel import create_engine, Session


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hw12_app"


engine = create_engine(
    DATABASE_URL,
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
        # FastAPI pattern

        # return session