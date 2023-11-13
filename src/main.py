from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

class Manutencao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    placa: str
    marca: str
    modelo: str
    cor: str
    nome_cliente: str
    nome_mecanico: str
    data_chegada: str
    data_finalizacao: Optional[str] = None

sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/manutencoes/")
def create_manutencao(manutencao: Manutencao):
    with SessionLocal() as session:
        session.add(manutencao)
        session.commit()
        session.refresh(manutencao)
        return manutencao
    
@app.patch("/manutencoes/{id}/finalizar")
def finalizar_manutencao(id:int):
    with Session(engine) as session:
        statament = select(Manutencao).where(Manutencao.id == id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
