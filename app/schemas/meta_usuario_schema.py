from pydantic import BaseModel

class MetaUsuarioCreateSchema(BaseModel):
    nome_usuario: str
    meta_litros: float  

class MetaUsuarioSchema(BaseModel):
    id: int
    nome_usuario: str
    meta_litros: float

    class Config:
        from_attributes = True
