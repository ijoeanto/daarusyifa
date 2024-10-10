from sqlalchemy import Column, Float, String, Integer , Text, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship

class Register(Base):
    __tablename__ = 'registers'

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    biaya = Column(String(50))
    poliklinik = Column(String(50))
    dokter = Column(String(50))
    tglkonsultasi = Column(String(20))
    jamkonsultasi = Column(String(20))
    sumber = Column(String(50))
    status = Column(String(50))
    idPasien = Column(Integer, ForeignKey('pasiens.id'))
    # idKajian = Column(Integer, ForeignKey('kajians.id'))

    klien = relationship('Pasien', back_populates='pendaftars')
    kajian = relationship('Kajian', back_populates='pengunjung')

class Pasien(Base):
    __tablename__ = 'pasiens'

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    telpon = Column(String(20))
    pekerjaan = Column(String(50))
    tgllahir = Column(String(20))
    sex = Column(String(20))
    nik = Column(String(20))
    goldarah = Column(String(5))
    alamat = Column(String(255))
    kodepos = Column(String(5))
    mrn = Column(String(10))
    status = Column(String(25))

    pendaftars = relationship('Register', back_populates='klien')
    keluhans = relationship('Kajian', back_populates='pelanggan')

class Kajian(Base):
    __tablename__ = 'kajians'

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    keluhan = Column(String(100))
    riwayat = Column(String(100))
    alergi = Column(String(100))
    suhu = Column(Float)
    sistole = Column(Float)
    diastole = Column(Float)
    nadi = Column(Integer)
    nafas = Column(Integer)
    tinggi = Column(Integer)
    berat = Column(Integer)
    imt = Column(Float)
    tglPemeriksaan = Column(String(20))
    anamnesa = Column(Text)
    diagnosa = Column(Text)
    terapi = Column(Text)
    tindakan = Column(Text)
    idPasien = Column(Integer, ForeignKey('pasiens.id'))
    idRegister = Column(Integer, ForeignKey('registers.id'))

    pelanggan = relationship('Pasien', back_populates='keluhans')
    pengunjung = relationship('Register', back_populates='kajian', cascade='all, delete', passive_deletes=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    password = Column(String(255))

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    firstname = Column(String(50))
    lastname = Column(String(50))
    password = Column(String(255))
    token = Column(String(255))
    role = Column(String(255))

    # peran = relationship('Role', back_populates='akuns', cascade='all, delete', passive_deletes=True)

class Medis(Base):
    __tablename__ = 'medis'

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    role = Column(String(50))
    sex = Column(String(20))
    telpon = Column(String(20))
    alamat = Column(String(255))
    kodepos = Column(String(20))
    status = Column(String(20))

# class Role(Base):
#     __tablename__ = 'roles'

#     id = Column(Integer, primary_key=True, index=True)
#     role = Column(Integer)

#     akuns = relationship('Account', back_populates='peran')