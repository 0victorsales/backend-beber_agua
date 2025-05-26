from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from app.database import get_db
from app.models.meta_consumo import MetaUsuario
from app.schemas.meta_usuario_schema import MetaUsuarioCreateSchema, MetaUsuarioSchema

router = APIRouter()

@router.post("/meta", response_model=MetaUsuarioSchema)
def registrar_meta(meta: MetaUsuarioCreateSchema, db: Session = Depends(get_db)):
    try:
        peso_kg = meta.peso_kg
        meta_litros = (peso_kg * 35) / 1000  

        meta_existente = db.query(MetaUsuario).filter(
            MetaUsuario.nome_usuario == meta.nome_usuario
        ).first()

        if meta_existente:
            meta_existente.meta_litros = meta_litros
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
                meta_litros=meta_litros
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
