from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Register
from schemas import ShowRegister, RegisterBase
from routers.authentication import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/register',
    tags=['Registrasi'],
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowRegister], dependencies=[Depends(get_current_user)])
async def getall (db:Session = Depends(get_db)):
    register = db.query(Register).order_by(Register.id.desc()).all()

    return register

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowRegister, dependencies=[Depends(get_current_user)])
async def all (id:int, db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.id == id).first()
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Registrasi tidak ditemukan!")

    return register

@router.get('/status/registrasi', status_code=status.HTTP_200_OK, response_model=List[RegisterBase], dependencies=[Depends(get_current_user)])
async def getbyregistrasi (db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.status.in_(('Registrasi', 'Pemeriksaan Awal', 'Terlayani'))).order_by(Register.id.desc()).all()
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Registrasi tidak ditemukan!")

    return register

@router.get('/status/reservasi', status_code=status.HTTP_200_OK, response_model=List[RegisterBase], dependencies=[Depends(get_current_user)])
async def getbyreservasi (db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.status.contains('Reservasi')).order_by(Register.id.desc()).all()
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Reservasi tidak ditemukan!")

    return register

@router.get('/status/terlayani', status_code=status.HTTP_200_OK, response_model=List[RegisterBase], dependencies=[Depends(get_current_user)])
async def getbyterlayani (db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.status.contains('Terlayani')).order_by(Register.id.desc()).all()
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Pasien tidak ditemukan!")

    return register

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create(request: RegisterBase, db:Session = Depends(get_db)):
    newRegister = Register(
                        nama=request.nama,
                        biaya=request.biaya,
                        poliklinik=request.poliklinik,
                        dokter=request.dokter,
                        tglkonsultasi=request.tglkonsultasi,
                        jamkonsultasi=request.jamkonsultasi,
                        sumber=request.sumber,
                        status=request.status,
                        idPasien=request.idPasien,
                    )
    db.add(newRegister)
    db.commit()
    db.refresh(newRegister)
    return newRegister

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=RegisterBase, dependencies=[Depends(get_current_user)])
async def update(id:int, request: RegisterBase, db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.id == id)
    if not register.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Registrasi tidak ditemukan!")
    
    register.update({
                    Register.nama:request.nama,
                    Register.biaya:request.biaya,
                    Register.poliklinik:request.poliklinik,
                    Register.dokter:request.dokter,
                    Register.tglkonsultasi:request.tglkonsultasi,
                    Register.jamkonsultasi:request.jamkonsultasi,
                    Register.sumber:request.sumber,
                    Register.status:request.status,
                    Register.idPasien:request.idPasien,
                })
    db.commit()
    data = db.query(Register).filter(Register.id == id).first()
    return data

@router.patch('/status/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=RegisterBase, dependencies=[Depends(get_current_user)])
async def updatestatus(id:int, request: RegisterBase, db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.id == id)
    if not register.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Registrasi tidak ditemukan!")
    
    register.update({
                    Register.nama:request.nama,
                    Register.biaya:request.biaya,
                    Register.poliklinik:request.poliklinik,
                    Register.dokter:request.dokter,
                    Register.tglkonsultasi:request.tglkonsultasi,
                    Register.jamkonsultasi:request.jamkonsultasi,
                    Register.sumber:request.sumber,
                    Register.status:request.status,
                    Register.idPasien:request.idPasien,
                })
    db.commit()
    data = db.query(Register).filter(Register.id == id).first()
    return data

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_current_user)])
async def delete_register(id:int, db:Session = Depends(get_db)):
    register = db.query(Register).filter(Register.id == id).first()
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Register tidak ditemukan")
    db.delete(register)
    db.commit()
    return {'success': 'Berhasil hapus data'}