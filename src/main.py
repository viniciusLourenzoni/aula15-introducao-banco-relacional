from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine

# ORM - Object Relational Mapping
# placa
# marca
# modelo
# cor
# nome cliente
# nome mecânico
# data e hora chegada
# data e hora finalização


class Manutencao(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    placa: str
    marca: str
    modelo: str
    cor: str
    nome_cliente: str
    nome_mecanico: str
    data_chegada: str
    data_finalizacao: Optional[str] = Field(default=None)


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "ok"}


@app.post("/manutencoes")
def cria_registro(manutencao: Manutencao):
    with Session(engine) as session:
        session.add(manutencao)
        session.commit()
        session.refresh(manutencao)
        return manutencao
