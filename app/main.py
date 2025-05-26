from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rotas import consumo_dia, consumo,historico, meta , progresso , registros_dias
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

 
app.include_router(consumo.router)
app.include_router(meta.router)
app.include_router(progresso.router)
app.include_router(historico.router)
app.include_router(registros_dias.router)
app.include_router(consumo_dia.router)

@app.get("/ping")
def ping():
    return {"mensagem": "pong"}

