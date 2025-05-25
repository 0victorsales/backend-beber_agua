# from fastapi import APIRouter, Query, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from app.database import get_db
# from app.models.consumo_diario import ConsumoDiario
# from app.models.meta_consumo import MetaUsuario
# from fastapi.responses import JSONResponse

# router = APIRouter()

# @router.get("/dias-com-registros")
# def dias_com_registros(nome_usuario: str = Query(...), db: Session = Depends(get_db)):
#     try:
#         datas = db.query(ConsumoDiario.data)\
#             .filter(ConsumoDiario.nome_usuario == nome_usuario)\
#             .distinct()\
#             .all()

#         dias = []
#         for (data,) in datas:
#             consumo_total_ml = db.query(func.sum(ConsumoDiario.consumo_ml)).filter(
#                 ConsumoDiario.nome_usuario == nome_usuario,
#                 ConsumoDiario.data == data
#             ).scalar() or 0

#             meta = db.query(MetaUsuario).filter(MetaUsuario.nome_usuario == nome_usuario).first()
#             meta_litros = meta.meta_litros if meta else 0

#             consumo_total_litros = consumo_total_ml / 1000
#             objetivo_alcancado = consumo_total_litros >= meta_litros if meta_litros > 0 else False

#             dias.append({
#                 "data": data.strftime("%Y-%m-%d"),
#                 "objetivoAlcancado": objetivo_alcancado
#             })

#         return JSONResponse(
#             status_code=200,
#             content={"dias": dias}
#         )

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"erro": f"Ocorreu um erro inesperado: {str(e)}"}
#         )
