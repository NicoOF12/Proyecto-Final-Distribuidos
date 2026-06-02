from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Reserva(BaseModel):
    nombre: str
    fecha: str


@app.get("/")
def root():
    return {
        "servicio": "app-core",
        "estado": "ok"
    }


@app.post("/validar-reserva")
def validar_reserva(reserva: Reserva):

    if not reserva.nombre.strip():
        return {
            "valida": False,
            "motivo": "Nombre vacío"
        }

    return {
        "valida": True
    }
