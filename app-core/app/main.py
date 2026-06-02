from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "servicio": "app-core",
        "estado": "ok"
    }


@app.get("/validar")
def validar():
    return {
        "resultado": "ok",
        "mensaje": "Validación realizada por app-core"
    }
