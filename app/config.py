import os
from dotenv import load_dotenv

load_dotenv()

class Configuracoes:
    PROJETO: str = "beber_agua"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///instance/database.db"

configuracoes = Configuracoes()
