from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from database import engine
from routers import pasien, register, kajian, authentication, account, medis

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(account.router)
app.include_router(pasien.router)
app.include_router(register.router)
app.include_router(kajian.router)
app.include_router(medis.router)