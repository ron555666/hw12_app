from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas import Token, UserCreate, UserResponse
from app.models import User
from app.database import get_session
from datetime import datetime
from app.dependency import DBSession
from app.security_utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth')


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: DBSession):
    # print('user', user)
    # return {'Message': "Success"}

    stmt = select(User).where(User.email == user.email)
    existing_user = db.exec(stmt).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered!"
        )
    
    db_user = User(
        email=user.email,
        username=user.username,
        hash_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
def login(db: DBSession, form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    if not verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password!"
        )
    
    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    access_token = create_access_token(user.id)

    return {'access_token': access_token}
