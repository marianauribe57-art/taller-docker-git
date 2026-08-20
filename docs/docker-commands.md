# Comandos Docker de referencia

> En Docker moderno se escribe `docker compose` (separado).
> La forma antigua `docker-compose` (con guion) hace lo mismo.

## Levantar y detener

```bash
docker compose up -d              # Levantar en segundo plano
docker compose up --build -d      # Reconstruir imágenes y levantar
docker compose down               # Detener y eliminar contenedores
docker compose down -v            # Además elimina los volúmenes (borra datos)
```

## Ver estado

```bash
docker compose ps                 # Contenedores del proyecto
docker compose logs -f            # Logs en vivo de todos los servicios
docker compose logs -f [servicio] # Logs de un servicio específico
docker ps                         # Todos los contenedores en ejecución
```

## Gestión

```bash
docker compose stop               # Detener sin eliminar
docker compose start              # Reanudar
docker compose restart [servicio] # Reiniciar un servicio
```

## Inspección

```bash
docker compose exec [servicio] sh       # Abrir shell dentro del contenedor
docker compose exec db psql -U postgres # Cliente de PostgreSQL
docker compose exec redis redis-cli     # Cliente de Redis
docker volume ls                        # Listar volúmenes
docker network ls                       # Listar redes
```

## Limpieza

```bash
docker system prune -f            # Eliminar recursos sin usar
docker volume prune -f            # Eliminar volúmenes huérfanos
docker compose down --rmi all -v  # Borrar todo lo del proyecto
```