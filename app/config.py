import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banco", "database.db")

class Configuracoes:
    PROJETO: str = "beber_agua"
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{DB_PATH}"

configuracoes = Configuracoes()


 

