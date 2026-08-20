# Escenario 1 - Ejercicio: WordPress + MariaDB + phpMyAdmin

Stack de WordPress con MariaDB como base de datos y phpMyAdmin para administrarla,
con todas las credenciales externalizadas en un archivo `.env`.

## Servicios

| Servicio | Imagen | Puerto | Descripción |
|----------|--------|--------|-------------|
| `db` | `mariadb:10.11` | interno | Base de datos |
| `wordpress` | `wordpress:latest` | 8082 | Sitio web |
| `phpmyadmin` | `phpmyadmin/phpmyadmin` | 8081 | Administrador de la BD |

## Configuración

Copiar la plantilla y completar los valores:

```bash
cp .env.example .env
```

## Uso

```bash
docker compose up -d       # Levantar
docker compose ps          # Ver estado
docker compose logs -f     # Ver logs
docker compose down        # Detener
docker compose down -v     # Detener y borrar los datos
```

## Acceso

- WordPress: http://localhost:8082
- phpMyAdmin: http://localhost:8081 (usuario y contraseña del `.env`)

## Persistencia

| Volumen | Contenido |
|---------|-----------|
| `mi_wordpress_data` | Datos de MariaDB |
| `mi_wordpress_html` | Archivos de WordPress (temas, plugins, uploads) |

Los datos sobreviven a `docker compose down`. Solo se borran con `down -v`.

## Red

Todos los servicios comparten la red `mi_red_wordpress` (driver bridge),
lo que les permite comunicarse por el nombre del servicio.