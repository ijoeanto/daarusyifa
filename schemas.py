from pydantic import BaseModel
from typing import List, Optional

class RegisterBase(BaseModel):
    id: int
    nama: str
    biaya: str 
    poliklinik: str 
    dokter: str 
    tglkonsultasi: str 
    jamkonsultasi: str 
    sumber: str 
    status: str 
    idPasien: int 
    
class Register(RegisterBase):
    class Config():
        from_attributes = True
        # orm_mode = True

class KajianBase(BaseModel):
    id: int
    nama: str 
    keluhan: str 
    riwayat: str 
    alergi: str 
    suhu: float
    sistole: float
    diastole: float
    nadi: int
    nafas: int
    tinggi: int
    berat: int
    imt: float
    tglPemeriksaan: str
    anamnesa: str
    diagnosa: str
    terapi: str
    tindakan: str
    idPasien: int
    idRegister: int

class Kajian(KajianBase):
    class Config():
        from_attributes = True
        
class Pasien(BaseModel):
    id: int
    nama: str
    telpon: str
    pekerjaan: str
    tgllahir: str
    sex: str
    nik: str
    goldarah: str
    alamat: str
    kodepos: str
    mrn: str
    status: str

class ShowKajianBase(BaseModel):
    id: int
    nama: str 
    keluhan: str 
    riwayat: str 
    alergi: str 
    suhu: float
    sistole: float
    diastole: float
    nadi: int
    nafas: int
    tinggi: int
    berat: int
    imt: float
    tglPemeriksaan: str
    anamnesa: str
    diagnosa: str
    terapi: str
    tindakan: str
    pelanggan: Pasien
    pengunjung: Register

    class Config():
        from_attributes = True

class ShowPasien(BaseModel):
    id: int
    nama: str
    telpon: str
    pekerjaan: str
    tgllahir: str
    sex: str
    nik: str
    goldarah: str
    alamat: str
    kodepos: str
    mrn: str
    status: str
    pendaftars: List[Register] = []
    keluhans: List[ShowKajianBase] = []
    # keluhans: List[Kajian] = []

    class Config():
        from_attributes = True
        # orm_mode = True
        
class ShowRegister(RegisterBase):
    klien: ShowPasien

    class Config():
        from_attributes = True
        # orm_mode = True

class ShowKajian(KajianBase):
    pelanggan: ShowPasien

    class Config():
        from_attributes = True

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str

class AccountBase(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    password: str
    token: str
    role: str

class UserAccount(BaseModel):
    username: str
    password: str

class RegisterAccount(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    password: str
    role: str

class ShowAccount(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    token: str
    role: str

# class RoleBase(BaseModel):
#     id: int
#     role: int

# class ShowRole(BaseModel):
#     id: int
#     role: int
#     akuns: List[ShowAccount] = []

#     class Config():
#         from_attributes = True

# class ShowAccountRole(BaseModel):
#     id: int
#     username: str
#     firstname: str
#     lastname: str
#     token: str
#     peran: ShowRole

#     class Config():
#         from_attributes = True

class MedisBase(BaseModel):
    id: int
    nama: str
    role: str
    sex: str
    telpon: str
    alamat: str
    kodepos: str
    status: str
