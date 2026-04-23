# User: id, email, username, password_hash
# Note: id, title, content, user_id, tags
# Tag: id, value
# AI endpoint, calling API for summarization

from sqlmodel import SQLModel, Field, Relationship, Session
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id : int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, max_length=255, index=True)
    username: str = Field(max_length=50)
    hash_password: str = Field(max_length=255)
    created_at: datetime = Field(default=datetime.now())

    notes: list['Note'] = Relationship(back_populates='user')


class Note(SQLModel,table=True):
    __tablename__ = 'notes'
    id : int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=50)
    # content: str = Field()
    content: str
    user_id: int = Field(foreign_key='users.id', index=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    user: User = Relationship(back_populates='notes')


