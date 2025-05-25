from fastapi import APIRouter, Depends
from app.schemas.consumo_diario_schema import ConsumoDiarioCreateSchema
from app.models.meta_consumo import MetaUsuario
from app.schemas.meta_usuario_schema import MetaUsuarioCreateSchema, MetaUsuarioSchema
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumo_diario import ConsumoDiario
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime
from fastapi import Query

router = APIRouter()

 

 

@router.post("/inserir-consumo")
def criar_consumo(consumo: ConsumoDiarioCreateSchema, db: Session = Depends(get_db)):
    try:
        hoje = datetime.now()
        data_atual = hoje.date()
        horario_atual = hoje.time()

        consumo_usuario = ConsumoDiario(
            nome_usuario=consumo.nome_usuario,
            consumo_ml=consumo.consumo_ml,
            data=data_atual,
            horario=horario_atual
        )

        db.add(consumo_usuario)
        db.commit()
        db.refresh(consumo_usuario)

        consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml))\
            .filter(
                ConsumoDiario.nome_usuario == consumo.nome_usuario,
                ConsumoDiario.data == data_atual
            ).scalar() or 0

        meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == consumo.nome_usuario).first()
        meta_litros = meta.meta_litros if meta else 0

        consumo_total_litros = consumo_total_ml / 1000   
        litros_faltantes = max(meta_litros - consumo_total_litros, 0)

        if meta_litros > 0:
            percentual_atingido = (consumo_total_litros / meta_litros) * 100
        else:
            percentual_atingido = 0

        return JSONResponse(
            status_code=201,
            content={
                "mensagem": "Consumo registrado com sucesso!",
                "dados": {
                    "nome_usuario": consumo_usuario.nome_usuario,
                    "data": str(consumo_usuario.data),
                    "horario": str(consumo_usuario.horario),
                    "consumo_ml": consumo_usuario.consumo_ml,
                    "consumo_total_hoje_ml": consumo_total_ml,
                    "meta_litros": meta_litros,
                    "litros_faltantes": litros_faltantes,
                    "percentual_atingido": round(percentual_atingido, 2)
                }
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
        )

@router.post("/registrar-meta", response_model=MetaUsuarioSchema)
def registrar_meta(meta: MetaUsuarioCreateSchema, db: Session = Depends(get_db)):
    try:
        meta_existente = db.query(MetaUsuario).filter(
            MetaUsuario.nome_usuario == meta.nome_usuario
        ).first()

        if meta_existente:
            meta_existente.meta_litros = meta.meta_litros
            db.commit()
            db.refresh(meta_existente)

            return JSONResponse(
                status_code=200,
                content={
                    "mensagem": "Meta atualizada com sucesso!",
                    "dados": {
                        "id": meta_existente.id,
                        "nome_usuario": meta_existente.nome_usuario,
                        "meta_litros": meta_existente.meta_litros
                    }
                }
            )
        else:
            nova_meta = MetaUsuario(
                nome_usuario=meta.nome_usuario,
                meta_litros=meta.meta_litros
            )
            db.add(nova_meta)
            db.commit()
            db.refresh(nova_meta)

            return JSONResponse(
                status_code=201,
                content={
                    "mensagem": "Meta registrada com sucesso!",
                    "dados": {
                        "id": nova_meta.id,
                        "nome_usuario": nova_meta.nome_usuario,
                        "meta_litros": nova_meta.meta_litros
                    }
                }
            )

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"erro": f"Erro ao registrar ou atualizar meta: {str(e)}"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
        )




@router.get("/consumos-dia")
def listar_consumos_hoje(nome_usuario: str = Query(..., description="Nome do usuário"), db: Session = Depends(get_db)):
    try:
        data_hoje = datetime.now().date()

        consumos = db.query(ConsumoDiario).filter(
            ConsumoDiario.nome_usuario == nome_usuario,
            ConsumoDiario.data == data_hoje
        ).all()

        lista_consumos = []
        for c in consumos:
            horario_formatado = c.horario.strftime("%H:%M")
            lista_consumos.append({
                "horario": horario_formatado,
                "consumo_ml": c.consumo_ml
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



@router.get("/progresso-hoje")
def progresso_hoje(
    nome_usuario: str = Query(..., description="Nome do usuário"),
    db: Session = Depends(get_db)
):
    try:
        data_hoje = datetime.now().date()

        consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml)).filter(
            ConsumoDiario.nome_usuario == nome_usuario,
            ConsumoDiario.data == data_hoje
        ).scalar() or 0

        meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == nome_usuario).first()
        meta_litros = meta.meta_litros if meta else 0

        consumo_total_litros = consumo_total_ml / 1000
        litros_faltantes = max(meta_litros - consumo_total_litros, 0)

        percentual_atingido = (consumo_total_litros / meta_litros) * 100 if meta_litros > 0 else 0

        return JSONResponse(
            status_code=200,
            content={
                "mensagem": f"Progresso de {nome_usuario} em {data_hoje}:",
                "dados": {
                    "consumo_total_hoje_ml": consumo_total_ml,
                    "meta_litros": meta_litros,
                    "litros_faltantes": litros_faltantes,
                    "percentual_atingido": percentual_atingido
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
        )



@router.get("/historico-dia")
def historico_dia(
    nome_usuario: str = Query(...),
    data: str = Query(...),   
    db: Session = Depends(get_db)
):
    try:
        data_objeto = datetime.strptime(data, "%Y-%m-%d").date()

        consumos = db.query(ConsumoDiario).filter(
            ConsumoDiario.nome_usuario == nome_usuario,
            ConsumoDiario.data == data_objeto
        ).all()

        registros = []
        for consumo in consumos:
            horario_formatado = consumo.horario.strftime("%H:%M")
            registros.append({
                "consumo_ml": consumo.consumo_ml,
                "horario": horario_formatado
            })

        meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == nome_usuario).first()
        meta_litros = meta.meta_litros if meta else 0

        consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml)).filter(
            ConsumoDiario.nome_usuario == nome_usuario,
            ConsumoDiario.data == data_objeto
        ).scalar() or 0

        consumo_total_litros = consumo_total_ml / 1000
        litros_faltantes = max(meta_litros - consumo_total_litros, 0)
        percentual_atingido = (consumo_total_litros / meta_litros) * 100 if meta_litros > 0 else 0

        return JSONResponse(
            status_code=200,
            content={
                "mensagem": f"Histórico de {nome_usuario} em {data}:",
                "registros": registros,
                "progresso": {
                    "consumo_total_hoje_ml": consumo_total_ml,
                    "meta_litros": meta_litros,
                    "litros_faltantes": litros_faltantes,
                    "percentual_atingido": percentual_atingido
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
        )



@router.get("/dias-com-registros")
def dias_com_registros(nome_usuario: str = Query(...), db: Session = Depends(get_db)):
    try:
        datas = db.query(ConsumoDiario.data)\
            .filter(ConsumoDiario.nome_usuario == nome_usuario)\
            .distinct()\
            .all()

        dias = []
        for (data,) in datas:
            consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml)).filter(
                ConsumoDiario.nome_usuario == nome_usuario,
                ConsumoDiario.data == data
            ).scalar() or 0

            meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == nome_usuario).first()
            meta_litros = meta.meta_litros if meta else 0

            consumo_total_litros = consumo_total_ml / 1000
            objetivo_alcancado = consumo_total_litros >= meta_litros if meta_litros > 0 else False

            dias.append({
                "data": data.strftime("%Y-%m-%d"),
                "objetivoAlcancado": objetivo_alcancado
            })

        return JSONResponse(
            status_code=200,
            content={"dias": dias}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
        )
