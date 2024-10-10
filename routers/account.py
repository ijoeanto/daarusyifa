from typing import Annotated, List
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from schemas import UserAccount, ShowAccount, RegisterAccount, TokenData
from fastapi import APIRouter, Depends, status, HTTPException
from passlib.hash import bcrypt
from passlib.context import CryptContext
from models import Account
from routers.authentication import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/account',
    tags=['Account'],
)

SECRET_KEY = '83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowAccount], dependencies=[Depends(get_current_user)])
async def getAll (db:Session = Depends(get_db)):
    account = db.query(Account).all()

    return account

@router.get('/user/me', status_code=status.HTTP_200_OK, response_model=ShowAccount)
def get_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
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
    except JWTError:
        raise credentials_exception
    user = db.query(Account).filter(Account.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
    
@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=ShowAccount, dependencies=[Depends(get_current_user)])
async def authenticate(request: UserAccount, db:Session = Depends(get_db)):
    user = db.query(Account).filter(Account.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Username Tidak ditemukan!")
    
    if not bcrypt.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Password salah!")
    
    return user

@router.post('/register', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_user(request: RegisterAccount, db:Session = Depends(get_db)):
    data={'sub': request.username}
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    newuser = Account(
                    username=request.username,
                    firstname=request.firstname,
                    lastname=request.lastname,
                    password=bcrypt.hash(request.password),
                    token=encoded_jwt,
                    role=request.role,
                )
    db.add(newuser)
    db.commit()
    return True

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ShowAccount, dependencies=[Depends(get_current_user)])
async def update(id:int, request: RegisterAccount, db:Session = Depends(get_db)):
    akun = db.query(Account).filter(Account.id == id)
    if not akun.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Akun tidak ditemukan!")
    
    akun.update({
                    Account.username:request.username,
                    Account.firstname:request.firstname,
                    Account.lastname:request.lastname,
                    Account.password:bcrypt.hash(request.password),
                    Account.role:request.role,
                })
    db.commit()
    data = db.query(Account).filter(Account.id == id).first()
    return data

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_current_user)])
async def delete_akun(id:int, db:Session = Depends(get_db)):
    akun = db.query(Account).filter(Account.id == id).first()
    if not akun:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Akun tidak ditemukan")
    db.delete(akun)
    db.commit()
    return {'success': 'Berhasil hapus data'}