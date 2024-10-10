from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Kajian
from schemas import ShowKajian, KajianBase
from routers.authentication import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/kajian',
    tags=['Kajian'],
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowKajian], dependencies=[Depends(get_current_user)])
async def getall (db:Session = Depends(get_db)):
    kajian = db.query(Kajian).all()

    return kajian

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowKajian, dependencies=[Depends(get_current_user)])
async def all (id:int, db:Session = Depends(get_db)):
    kajian = db.query(Kajian).filter(Kajian.id == id).first()
    if not kajian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Pemeriksaan tidak ditemukan!")

    return kajian

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create(request: KajianBase, db:Session = Depends(get_db)):
    newKajian = Kajian(
                        nama=request.nama,
                        keluhan=request.keluhan,
                        riwayat=request.riwayat,
                        alergi=request.alergi,
                        suhu=request.suhu,
                        sistole=request.sistole,
                        diastole=request.diastole,
                        nadi=request.nadi,
                        nafas=request.nafas,
                        tinggi=request.tinggi,
                        berat=request.berat,
                        imt=request.imt,
                        tglPemeriksaan=request.tglPemeriksaan,
                        anamnesa=request.anamnesa,
                        diagnosa=request.diagnosa,
                        terapi=request.terapi,
                        tindakan=request.tindakan,
                        idPasien=request.idPasien,
                        idRegister=request.idRegister
                    )
    db.add(newKajian)
    db.commit()
    db.refresh(newKajian)
    return newKajian

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=KajianBase, dependencies=[Depends(get_current_user)])
async def update(id:int, request: KajianBase, db:Session = Depends(get_db)):
    kajian = db.query(Kajian).filter(Kajian.id == id)
    if not kajian.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Pemeriksaan tidak ditemukan!")
    
    kajian.update({
                    Kajian.nama:request.nama,
                    Kajian.keluhan:request.keluhan,
                    Kajian.riwayat:request.riwayat,
                    Kajian.alergi:request.alergi,
                    Kajian.suhu:request.suhu,
                    Kajian.sistole:request.sistole,
                    Kajian.diastole:request.diastole,
                    Kajian.nadi:request.nadi,
                    Kajian.nafas:request.nafas,
                    Kajian.tinggi:request.tinggi,
                    Kajian.berat:request.berat,
                    Kajian.imt:request.imt,
                    Kajian.tglPemeriksaan:request.tglPemeriksaan,
                    Kajian.anamnesa:request.anamnesa,
                    Kajian.diagnosa:request.diagnosa,
                    Kajian.terapi:request.terapi,
                    Kajian.tindakan:request.tindakan,
                    Kajian.idPasien:request.idPasien,
                })
    db.commit()
    data = db.query(Kajian).filter(Kajian.id == id).first()
    return data


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_current_user)])
async def delete_kajian(id:int, db:Session = Depends(get_db)):
    kajian = db.query(Kajian).filter(Kajian.id == id).first()
    if not kajian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Kajian tidak ditemukan")
    db.delete(kajian)
    db.commit()
    return {'success': 'Berhasil hapus data'}

@router.get('/date/count', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def allCount (db:Session = Depends(get_db)):
    kajian = db.query(Kajian.tglPemeriksaan, func.count(Kajian.tglPemeriksaan)).group_by(Kajian.tglPemeriksaan).all()
    if not kajian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Registrasi tidak ditemukan!")

    return kajian
