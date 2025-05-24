import os
from dotenv import load_dotenv

load_dotenv()

class Configuracoes:
    PROJETO: str = "beber_agua"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///C:/Users/SAMSUNG/Desktop/parceiro/PYTHON/backend-beber_agua/app/banco/database.db"


configuracoes = Configuracoes()


 

