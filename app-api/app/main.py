from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

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


Base.metadata.create_all(bind=engine)


class ReservaCreate(BaseModel):
    nombre: str
    fecha: str


app = FastAPI()


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}


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
