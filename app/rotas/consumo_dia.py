from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumo_diario import ConsumoDiario
from fastapi.responses import JSONResponse
from sqlalchemy import func
from datetime import datetime
from fastapi import Query

router = APIRouter()

 


@router.get("/consumos-dia")
def listar_consumos_hoje(nome_usuario: str = Query(..., description="Nome do usuário"), db: Session = Depends(get_db)):
    try:
        data_hoje = datetime.now().date()

        consumos = db.query(ConsumoDiario).filter(
            ConsumoDiario.nome_usuario == nome_usuario,
            ConsumoDiario.data == data_hoje
        ).all()

        lista_consumos = []
        for consumo in consumos:
            horario_formatado = consumo.horario.strftime("%H:%M")
            lista_consumos.append({
                "horario": horario_formatado,
                "consumo_ml": consumo.consumo_ml
            })

        return JSONResponse(
            status_code=200,
            content={
                "mensagem": f"Consumos do usuário {nome_usuario} em {data_hoje}:",
                "consumos": lista_consumos
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
        )
