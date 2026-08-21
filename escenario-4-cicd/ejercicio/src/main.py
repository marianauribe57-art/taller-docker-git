import os

from fastapi import FastAPI

VERSION = os.environ.get("APP_VERSION", "1.0.0")
ENTORNO = os.environ.get("ENTORNO", "development")

app = FastAPI(
    title="App CI/CD",
    description="Aplicacion de ejemplo para el pipeline de CI/CD",
    version=VERSION
)


@app.get("/")
def index():
    return {
        "mensaje": "Hola desde Docker + CI/CD!",
        "version": VERSION,
        "entorno": ENTORNO,
        "autora": "Mariana Uribe - SENA"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/version")
def version():
    return {"version": VERSION}


@app.get("/suma/{a}/{b}")
def suma(a: int, b: int):
    return {"a": a, "b": b, "resultado": a + b}