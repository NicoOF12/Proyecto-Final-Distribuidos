from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from prometheus_fastapi_instrumentator import Instrumentator
import requests

DATABASE_URL = "postgresql://appuser:app123@10.10.0.12:5432/appdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha = Column(String, nullable=False)

class Recurso(Base):
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)


class ReservaCreate(BaseModel):
    nombre: str
    fecha: str

class RecursoCreate(BaseModel):
    nombre: str
    tipo: str

class Login(BaseModel):
    usuario: str
    password: str

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

@app.post("/login")
def login(datos: Login):

    if (
        datos.usuario == "admin"
        and
        datos.password == "admin123"
    ):
        return {
            "mensaje": "Login correcto",
            "usuario": datos.usuario
        }

    return {
        "mensaje": "Credenciales inválidas"
    }

@app.get("/reservas")
def listar_reservas():
    db = SessionLocal()

    reservas = db.query(Reserva).all()

    resultado = []

    for r in reservas:
        resultado.append(
            {
                "id": r.id,
                "nombre": r.nombre,
                "fecha": r.fecha
            }
        )

    db.close()

    return resultado

@app.get("/validacion")
def validar_con_core():

    respuesta = requests.get(
        "http://10.10.0.11:8001/validar",
        timeout=5
    )

    return respuesta.json()

@app.post("/reservas")
def crear_reserva(reserva: ReservaCreate):
    db = SessionLocal()

    nueva = Reserva(
        nombre=reserva.nombre,
        fecha=reserva.fecha
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    db.close()

    return {
        "mensaje": "Reserva creada",
        "id": nueva.id
    }


@app.delete("/reservas/{id}")
def eliminar_reserva(id: int):
    db = SessionLocal()

    reserva = db.query(Reserva).filter(
        Reserva.id == id
    ).first()

    if reserva:
        db.delete(reserva)
        db.commit()

    db.close()

    return {"mensaje": "Reserva eliminada"}

@app.post("/recursos")
def crear_recurso(recurso: RecursoCreate):
    db = SessionLocal()

    nueva = Recurso(
        nombre=recurso.nombre,
        tipo=recurso.tipo
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    db.close()

    return {
        "mensaje": "Recurso creado",
        "id": nueva.id
    }

@app.get("/recursos")
def listar_recursos():
    db = SessionLocal()

    recursos = db.query(Recurso).all()

    resultado = []

    for r in recursos:
        resultado.append(
            {
                "id": r.id,
                "nombre": r.nombre,
                "tipo": r.tipo
            }
        )

    db.close()

    return resultado

@app.delete("/recursos/{id}")
def eliminar_recurso(id: int):
    db = SessionLocal()

    recurso = db.query(Recurso).filter(
        Recurso.id == id
    ).first()

    if recurso:
        db.delete(recurso)
        db.commit()

    db.close()

    return {"mensaje": "Recurso eliminado"}
