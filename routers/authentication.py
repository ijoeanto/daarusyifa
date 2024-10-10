from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from schemas import TokenData, Token, User as UserBase
from fastapi import APIRouter, Depends, status, HTTPException
from passlib.hash import bcrypt
from passlib.context import CryptContext
from models import User

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=['Token'])

SECRET_KEY = '83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user(username: str, db:Session = Depends(get_db)):#still
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    
@router.get('/user/me')
async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='token has been expired'
        )
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post('/verif', dependencies=[Depends(get_current_user)])
async def verify_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    
    if not bcrypt.verify(password, user.password):
        return False
    
    return True

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
    # else:
    #     expire = datetime.now(timezone.utc) + timedelta(minutes=1)

    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/token', response_model=Token)
async def token_generate(form_data: OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    user = await verify_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(data={'sub': form_data.username}, expires_delta=access_token_expires)
    access_token = create_access_token(data={'sub': form_data.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/user', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_user(request: UserBase, db:Session = Depends(get_db)):
    newuser = User(
                    username=request.username,
                    password=bcrypt.hash(request.password)
                )
    db.add(newuser)
    db.commit()
    return True