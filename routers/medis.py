from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Medis
from schemas import MedisBase
from routers.authentication import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/medis',
    tags=['Medis'],
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[MedisBase], dependencies=[Depends(get_current_user)])
async def getAll (db:Session = Depends(get_db)):
    medis = db.query(Medis).all()

    return medis

@router.get('/groupby/{col}', status_code=status.HTTP_200_OK, response_model=List[MedisBase], dependencies=[Depends(get_current_user)])
async def getAllbyGroup (col:str, db:Session = Depends(get_db)):
    medis = db.query(Medis).group_by(col).all()

    return medis

@router.get('/filterby/{col}', status_code=status.HTTP_200_OK, response_model=List[MedisBase], dependencies=[Depends(get_current_user)])
async def getAllFilterbyColumn (col:str, db:Session = Depends(get_db)):
    medis = db.query(Medis).filter(Medis.role == col).all()

    return medis

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=MedisBase, dependencies=[Depends(get_current_user)])
async def all (id:int, db:Session = Depends(get_db)):
    medis = db.query(Medis).filter(Medis.id == id).first()
    if not medis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Medis tidak ditemukan!")

    return medis

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create(request: MedisBase, db:Session = Depends(get_db)):
    newMedis = Medis(
                        nama=request.nama,
                        role=request.role,
                        sex=request.sex,
                        telpon=request.telpon,
                        alamat=request.alamat,
                        kodepos=request.kodepos,
                        status=request.status,
                    )
    db.add(newMedis)
    db.commit()
    db.refresh(newMedis)
    return newMedis

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=MedisBase, dependencies=[Depends(get_current_user)])
async def update(id:int, request: MedisBase, db:Session = Depends(get_db)):
    medis = db.query(Medis).filter(Medis.id == id)
    if not medis.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Medis tidak ditemukan!")
    
    medis.update({
                    Medis.nama:request.nama,
                    Medis.role:request.role,
                    Medis.sex:request.sex,
                    Medis.telpon:request.telpon,
                    Medis.alamat:request.alamat,
                    Medis.kodepos:request.kodepos,
                    Medis.status:request.status
                })
    db.commit()
    data = db.query(Medis).filter(Medis.id == id).first()
    return data

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_current_user)])
async def delete_medis(id:int, db:Session = Depends(get_db)):
    medis = db.query(Medis).filter(Medis.id == id).first()
    if not medis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Medis tidak ditemukan")
    db.delete(medis)
    db.commit()
    return {'success': 'Berhasil hapus data'}