from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Pasien
from schemas import ShowPasien, Pasien as PasienBase
from routers.authentication import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/pasien',
    tags=['Pasien'],
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowPasien], dependencies=[Depends(get_current_user)])
async def getall (db:Session = Depends(get_db)):
    pasien = db.query(Pasien).all()

    return pasien

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PasienBase, dependencies=[Depends(get_current_user)])
async def all (id:int, db:Session = Depends(get_db)):
    pasien = db.query(Pasien).filter(Pasien.id == id).first()
    if not pasien:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Pasien tidak ditemukan!")

    return pasien

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create(request: PasienBase, db:Session = Depends(get_db)):
    newPasien = Pasien(
                        nama=request.nama,
                        telpon=request.telpon,
                        pekerjaan=request.pekerjaan,
                        tgllahir=request.tgllahir,
                        sex=request.sex,
                        nik=request.nik,
                        goldarah=request.goldarah,
                        alamat=request.alamat,
                        kodepos=request.kodepos,
                        mrn=request.mrn,
                        status=request.status,
                    )
    db.add(newPasien)
    db.commit()
    db.refresh(newPasien)
    return newPasien

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PasienBase, dependencies=[Depends(get_current_user)])
async def update(id:int, request: PasienBase, db:Session = Depends(get_db)):
    pasien = db.query(Pasien).filter(Pasien.id == id)
    if not pasien.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Pasien tidak ditemukan!")
    
    pasien.update({
                    Pasien.nama:request.nama,
                    Pasien.telpon:request.telpon,
                    Pasien.pekerjaan:request.pekerjaan,
                    Pasien.tgllahir:request.tgllahir,
                    Pasien.sex:request.sex,
                    Pasien.nik:request.nik,
                    Pasien.goldarah:request.goldarah,
                    Pasien.alamat:request.alamat,
                    Pasien.kodepos:request.kodepos,
                    Pasien.mrn:request.mrn,
                    Pasien.status:request.status
                })
    db.commit()
    data = db.query(Pasien).filter(Pasien.id == id).first()
    return data

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_current_user)])
async def delete_pasien(id:int, db:Session = Depends(get_db)):
    pasien = db.query(Pasien).filter(Pasien.id == id).first()
    if not pasien:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Pasien tidak ditemukan")
    db.delete(pasien)
    db.commit()
    return {'success': 'Berhasil hapus data'}