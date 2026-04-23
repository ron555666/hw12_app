from sqlmodel import SQLModel, Session
from database import engine
from models import User, Note

def create_tables():
    SQLModel.metadata.create_all(engine)

create_tables()

with Session(engine) as session:
    user = User(
        email='admin@example.com',
        username='admin user',
        hash_password='initialpassword'
    )
    session.add(user)
    session.commit()

    print(f'Created user {user.id} {user.username}')
    if user.id:
        note = Note(
            title="First note",
            content='Python lesson',
            user_id=user.id
        )
        session.add(note)
        session.commit()
        print(f'Session added {note.id}')