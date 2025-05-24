from pydantic import BaseModel
from datetime import date, time

class ConsumoDiarioSchema(BaseModel):
    nome_usuario: str
    data: date
    horario: time
    consumo_ml: int

    class Config:
        orm_mode = True