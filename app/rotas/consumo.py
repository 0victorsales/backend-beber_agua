from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumo_diario import ConsumoDiario
from app.models.meta_consumo import MetaUsuario
from sqlalchemy import func
from datetime import datetime
from app.schemas.consumo_diario_schema import ConsumoDiarioCreateSchema
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/consumo")
def criar_consumo(consumo: ConsumoDiarioCreateSchema, db: Session = Depends(get_db)):
    try:
        hoje = datetime.now()
        data_atual = hoje.date()
        horario_atual = hoje.time()

        novo_consumo = ConsumoDiario(
            nome_usuario=consumo.nome_usuario,
            consumo_ml=consumo.consumo_ml,
            data=data_atual,
            horario=horario_atual
        )

        db.add(novo_consumo)
        db.commit()
        db.refresh(novo_consumo)

        consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml)).filter(
            ConsumoDiario.nome_usuario == consumo.nome_usuario,
            ConsumoDiario.data == data_atual
        ).scalar() or 0

        meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == consumo.nome_usuario).first()
        meta_litros = meta.meta_litros if meta else 0
        consumo_total_litros = consumo_total_ml / 1000
        litros_faltantes = max(meta_litros - consumo_total_litros, 0)
        percentual_atingido = (consumo_total_litros / meta_litros) * 100 if meta_litros > 0 else 0

        return JSONResponse(
            status_code=201,
            content={
                "mensagem": "Consumo registrado com sucesso!",
                "dados": {
                    "nome_usuario": novo_consumo.nome_usuario,
                    "data": str(novo_consumo.data),
                    "horario": str(novo_consumo.horario),
                    "consumo_ml": novo_consumo.consumo_ml,
                    "consumo_total_hoje_ml": consumo_total_ml,
                    "meta_litros": meta_litros,
                    "litros_faltantes": litros_faltantes,
                    "percentual_atingido": round(percentual_atingido, 2)
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"erro": str(e)})
