from sqlalchemy import Column, Integer, String, Date, Time, Float
from app.database import Base

class ConsumoDiario(Base):
    __tablename__ = "consumo_diario"

    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(100), nullable=False)
    data = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)
    consumo_ml = Column(Float, nullable=False)
