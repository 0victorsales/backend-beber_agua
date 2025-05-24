from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import configuracoes

engine = create_engine(
    configuracoes.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

sessao = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessao()
    try:
        yield db
    finally:
        db.close()