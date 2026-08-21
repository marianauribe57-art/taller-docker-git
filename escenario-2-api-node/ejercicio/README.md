# Escenario 2 - Ejercicio: API REST de Usuarios

API REST CRUD en Node.js + Express conectada a PostgreSQL, con pgAdmin
para administrar la base de datos. Credenciales externalizadas en `.env`.

## Servicios

| Servicio | Imagen | Puerto | Descripción |
|----------|--------|--------|-------------|
| `db` | `postgres:15-alpine` | interno | Base de datos |
| `api` | build local | 3001 | API REST |
| `pgadmin` | `dpage/pgadmin4` | 5050 | Administrador de PostgreSQL |

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/usuarios` | Listar todos |
| GET | `/usuarios/:id` | Consultar uno |
| POST | `/usuarios` | Crear |
| PUT | `/usuarios/:id` | Actualizar |
| DELETE | `/usuarios/:id` | Eliminar |

## Validaciones

- `nombre`: obligatorio, mínimo 3 caracteres
- `email`: obligatorio, formato válido, único en la base de datos

Códigos de respuesta: `400` datos inválidos, `404` no encontrado,
`409` email duplicado.

## Migraciones

El script `init-scripts/01-init.sql` se ejecuta automáticamente la primera
vez que arranca PostgreSQL: crea la tabla `usuarios`, un índice sobre
`email` e inserta datos de prueba.

## Uso

```bash
cp .env.example .env     # completar valores
docker compose up --build -d
docker compose logs -f api
docker compose down
```

También hay un `Makefile` con atajos: `make up`, `make down`, `make logs`, `make clean`.

## Acceso

- API: http://localhost:3001/health
- pgAdmin: http://localhost:5050 (credenciales del `.env`)

## Persistencia

| Volumen | Contenido |
|---------|-----------|
| `pg_usuarios_data` | Datos de PostgreSQL |
| `pgadmin_data` | Configuración de pgAdmin |