from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rotas import rotas
from app.database import Base, engine

app = FastAPI(title="beber_agua")

 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 
Base.metadata.create_all(bind=engine)

 
app.include_router(rotas.router)

@app.get("/ping")
def ping():
    return {"mensagem": "pong"}

