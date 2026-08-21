import json
import os
import time

import psycopg2
import psycopg2.extras
import redis
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="API con cache Redis",
    description="PostgreSQL como fuente de verdad, Redis como capa de cache",
    version="1.0.0"
)

# ---------- Configuracion ----------
CACHE_TTL = int(os.environ.get("CACHE_TTL", 60))
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", 10))
RATE_WINDOW = int(os.environ.get("RATE_WINDOW", 60))

redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)


def conectar_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", 5432),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        dbname=os.environ.get("POSTGRES_DB")
    )


# ---------- Rate limiting ----------
@app.middleware("http")
async def rate_limiting(request: Request, call_next):
    # El health no se limita, para no romper el healthcheck de Docker
    if request.url.path == "/health":
        return await call_next(request)

    ip = request.client.host
    clave = f"rate:{ip}"

    try:
        peticiones = redis_client.incr(clave)
        if peticiones == 1:
            redis_client.expire(clave, RATE_WINDOW)

        if peticiones > RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Demasiadas peticiones",
                    "limite": f"{RATE_LIMIT} por {RATE_WINDOW} segundos",
                    "reintentar_en": redis_client.ttl(clave)
                }
            )
    except redis.RedisError:
        # Si Redis se cae, la API sigue funcionando sin limite
        pass

    respuesta = await call_next(request)
    respuesta.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
    return respuesta


# ---------- Modelos ----------
class UsuarioIn(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


# ---------- Endpoints ----------
@app.get("/")
def index():
    return {"servicio": "API con cache Redis", "docs": "/docs"}


@app.get("/health")
def health():
    estado = {"api": "OK"}
    try:
        redis_client.ping()
        estado["redis"] = "OK"
    except redis.RedisError:
        estado["redis"] = "ERROR"
    try:
        conn = conectar_db()
        conn.close()
        estado["postgres"] = "OK"
    except psycopg2.Error:
        estado["postgres"] = "ERROR"
    return estado


@app.get("/contador")
def contador():
    """Contador de visitas usando INCR de Redis"""
    visitas = redis_client.incr("contador:visitas")
    return {"visitas": visitas}


@app.get("/usuarios")
def listar_usuarios():
    """Patron cache-aside: primero Redis, si no esta va a PostgreSQL"""
    clave = "usuarios:todos"
    inicio = time.time()

    en_cache = redis_client.get(clave)
    if en_cache:
        return {
            "origen": "cache",
            "ttl_restante": redis_client.ttl(clave),
            "tiempo_ms": round((time.time() - inicio) * 1000, 2),
            "usuarios": json.loads(en_cache)
        }

    conn = conectar_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, nombre, email FROM usuarios ORDER BY id")
    usuarios = [dict(fila) for fila in cur.fetchall()]
    cur.close()
    conn.close()

    redis_client.setex(clave, CACHE_TTL, json.dumps(usuarios))

    return {
        "origen": "postgresql",
        "cacheado_por": f"{CACHE_TTL} segundos",
        "tiempo_ms": round((time.time() - inicio) * 1000, 2),
        "usuarios": usuarios
    }


@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioIn):
    """Inserta en PostgreSQL e invalida el cache"""
    try:
        conn = conectar_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id, nombre, email",
            (usuario.nombre.strip(), usuario.email.lower())
        )
        nuevo = dict(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    redis_client.delete("usuarios:todos")
    return {"mensaje": "Usuario creado, cache invalidado", "usuario": nuevo}


@app.get("/cache/estadisticas")
def estadisticas():
    info = redis_client.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    return {
        "keys_totales": redis_client.dbsize(),
        "memoria_usada": info.get("used_memory_human"),
        "hits": hits,
        "misses": misses,
        "tasa_aciertos": f"{round(hits / total * 100, 2)}%" if total else "sin datos"
    }


@app.delete("/cache")
def limpiar_cache():
    redis_client.flushdb()
    return {"mensaje": "Cache limpiado"}