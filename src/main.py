from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

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


@app.patch("/manutencoes/{id}/finalizar")
def finalizar_manutencao(id: int):
    with Session(engine) as session:
        # Monta a query = SELECT * FROM manutencao where id = id
        statement = select(Manutencao).where(Manutencao.id == id)
        manutencao = session.exec(statement=statement).first()
        # validar se a manutenção ainda está em aberto
        if manutencao.data_finalizacao:
            return JSONResponse(
                content={"message": "Manutenção já finalizada"},
                status_code=HTTPStatus.BAD_REQUEST,
            )

        # atualizar a data_finalizacao com a data atual
        manutencao.data_finalizacao = str(datetime.now())
        # aplica a alteração no banco
        session.commit()
        # Atualiza o registro a partir
        session.refresh(manutencao)
        return manutencao


# DELETE /manutencoes/id
# Só pode deletar uma manutencao que ainda não tenha sido finalizada


@app.delete("/manutencoes/{id}")
def deletar_manutencao(id: int):
    with Session(engine) as session:
        # Monta a query = SELECT * FROM manutencao where id = id
        statement = select(Manutencao).where(Manutencao.id == id)

        # Executa a query e retorna o registro ou None se não existir
        manutencao = session.exec(statement=statement).first()

        print(manutencao)
        # Valida se existe a manutenção
        if not manutencao:
            return JSONResponse(
                content={"message": "Manutenção não existe"},
                status_code=HTTPStatus.NOT_FOUND,
            )

        # Valida se a manutenção já foi finalizada
        if manutencao.data_finalizacao:
            return JSONResponse(
                content={"message": "Manutenção já finalizada"},
                status_code=HTTPStatus.BAD_REQUEST,
            )

        session.delete(manutencao)
        session.commit()
        return JSONResponse(
            content=None,
            status_code=HTTPStatus.NO_CONTENT,
        )
