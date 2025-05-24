from sqlalchemy import Column, Integer, String,Float
from app.database import Base

class MetaUsuario(Base):
    __tablename__ = "meta_usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(100), nullable=False)
    meta_litros = Column(Float, nullable=False)  
