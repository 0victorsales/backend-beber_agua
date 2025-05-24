from fastapi import APIRouter, Depends, HTTPException
from app.schemas.consumo_diario_schema import ConsumoDiarioSchema
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumo_diario import ConsumoDiario
from typing import List

router = APIRouter()

 

 

@router.post("/inserir-consumo", response_model=ConsumoDiarioSchema)
def criar_consumo(consumo: ConsumoDiarioSchema, db: Session = Depends(get_db)):
    novo_consumo = ConsumoDiario(**consumo.dict())
    db.add(novo_consumo)
    db.commit()
    db.refresh(novo_consumo)
    return novo_consumo



@router.get("/", response_model=List[ConsumoDiarioSchema])
def listar_consumos(db: Session = Depends(get_db)):
    return db.query(ConsumoDiario).all()
