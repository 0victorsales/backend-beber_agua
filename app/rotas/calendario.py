# from fastapi import APIRouter, Query, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from app.database import get_db
# from app.models.meta_consumo import MetaUsuario
# from app.models.consumo_diario import ConsumoDiario
# from fastapi.responses import JSONResponse
# from datetime import datetime

# router = APIRouter()

# @router.get("/historico-dia")
# def historico_dia(
#     nome_usuario: str = Query(...),
#     data: str = Query(...),   
#     db: Session = Depends(get_db)
# ):
#     try:
#         data_objeto = datetime.strptime(data, "%Y-%m-%d").date()

#         consumos = db.query(ConsumoDiario).filter(
#             ConsumoDiario.nome_usuario == nome_usuario,
#             ConsumoDiario.data == data_objeto
#         ).all()

#         registros = []
#         for consumo in consumos:
#             horario_formatado = consumo.horario.strftime("%H:%M")
#             registros.append({
#                 "consumo_ml": consumo.consumo_ml,
#                 "horario": horario_formatado
#             })

#         meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == nome_usuario).first()
#         meta_litros = meta.meta_litros if meta else 0

#         consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml)).filter(
#             ConsumoDiario.nome_usuario == nome_usuario,
#             ConsumoDiario.data == data_objeto
#         ).scalar() or 0

#         consumo_total_litros = consumo_total_ml / 1000
#         litros_faltantes = max(meta_litros - consumo_total_litros, 0)
#         percentual_atingido = (consumo_total_litros / meta_litros) * 100 if meta_litros > 0 else 0

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "mensagem": f"Histórico de {nome_usuario} em {data}:",
#                 "registros": registros,
#                 "progresso": {
#                     "consumo_total_hoje_ml": consumo_total_ml,
#                     "meta_litros": meta_litros,
#                     "litros_faltantes": litros_faltantes,
#                     "percentual_atingido": percentual_atingido
#                 }
#             }
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
#         )
