# Escenario 3 - Ejercicio: Caché con Redis + FastAPI

API en FastAPI que usa PostgreSQL como fuente de verdad y Redis como capa
de caché, con rate limiting y configuración separada de desarrollo y producción.

## Servicios

| Servicio | Imagen | Puerto (dev) | Descripción |
|----------|--------|--------------|-------------|
| `db` | `postgres:15-alpine` | 5433 | Fuente de verdad |
| `redis` | `redis:7-alpine` | 6380 | Caché y rate limiting |
| `app` | build local | 8000 | API FastAPI |
| `redis-commander` | `rediscommander/redis-commander` | 8081 | Inspector de Redis (solo dev) |

Todos los servicios tienen `healthcheck` configurado.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información del servicio |
| GET | `/health` | Estado de API, Redis y PostgreSQL |
| GET | `/contador` | Contador de visitas con `INCR` |
| GET | `/usuarios` | Listado con patrón cache-aside |
| POST | `/usuarios` | Crear usuario e invalidar caché |
| GET | `/cache/estadisticas` | Hits, misses y tasa de aciertos |
| DELETE | `/cache` | Limpiar el caché |
| GET | `/docs` | Documentación interactiva (Swagger) |

## Patrón cache-aside

1. La petición llega a `/usuarios`
2. Se busca la llave `usuarios:todos` en Redis
3. Si existe → se devuelve desde caché (`origen: cache`)
4. Si no existe → se consulta PostgreSQL, se guarda en Redis con TTL y se devuelve (`origen: postgresql`)
5. Al crear un usuario, la llave se elimina para que el caché no quede desactualizado

## Rate limiting

Máximo 10 peticiones por minuto por dirección IP, implementado con `INCR` y
`EXPIRE` de Redis. Al superarlo devuelve `429 Too Many Requests`.
La ruta `/health` está exenta para no interferir con el healthcheck de Docker.

## Desarrollo vs Producción

```bash
# Desarrollo: usa docker-compose.yml + docker-compose.override.yml
docker compose up --build -d

# Producción: solo el archivo base
docker compose -f docker-compose.yml up --build -d
```

| | Desarrollo | Producción |
|---|---|---|
| Recarga automática | Sí (`--reload`) | No |
| Puertos de db y redis | Expuestos | Internos |
| Redis Commander | Sí | No |

## Uso

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
docker compose logs -f app
docker compose down
```

## Acceso

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Redis Commander: http://localhost:8081