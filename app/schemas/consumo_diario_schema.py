from pydantic import BaseModel

class ConsumoDiarioCreateSchema(BaseModel):
    nome_usuario: str
    consumo_ml: float

class ConsumoDiarioSchema(BaseModel):
    nome_usuario: str
    data: str
    horario: str
    consumo_ml: float

    class Config:
        from_attributes = True
