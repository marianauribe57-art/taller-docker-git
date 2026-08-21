# Escenario 4 - Ejercicio: CI/CD con GitHub Actions

[![CI/CD - Escenario 4](https://github.com/marianauribe57-art/taller-docker-git/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/marianauribe57-art/taller-docker-git/actions/workflows/ci-cd.yml)

Aplicación en FastAPI con pipeline de integración y despliegue continuo:
tests automáticos, escaneo de vulnerabilidades y publicación de la imagen
en DockerHub y GitHub Container Registry.

## Pipeline

El workflow vive en `.github/workflows/ci-cd.yml` (raíz del repositorio,
que es donde GitHub Actions los busca) y tiene tres trabajos:

| Trabajo | Qué hace |
|---------|----------|
| `test` | Instala dependencias y ejecuta 6 pruebas con pytest |
| `seguridad` | Escanea dependencias y configuración con Trivy |
| `build-push` | Construye la imagen y la publica — **solo si los dos anteriores pasaron** |

`test` y `seguridad` corren en paralelo. `build-push` declara
`needs: [test, seguridad]`, así que una prueba fallida detiene la publicación.

### Cuándo se ejecuta

- Push a `main` o `develop`
- Tags que empiecen por `v` (ej: `v1.0.0`)
- Pull requests hacia `main` (solo tests y escaneo, sin publicar)
- Manualmente, desde la pestaña Actions

## Registros de imágenes

| Registro | Imagen |
|----------|--------|
| DockerHub | `marianamumm/app-cicd-sena` |
| GHCR | `ghcr.io/marianauribe57-art/app-cicd-sena` |

### Tags semánticos

Al publicar un tag `v1.2.3`, la acción `metadata-action` genera
automáticamente `1.2.3`, `1.2` y `latest`.

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Multi-stage build

El `Dockerfile` tiene dos etapas:

1. **builder** — instala las dependencias de Python
2. **production** — copia solo lo instalado, sin herramientas de construcción

La imagen final además corre con el usuario `appuser`, sin privilegios de root,
y tiene `HEALTHCHECK` propio.

## Uso local

```bash
# Desarrollo: construye la imagen localmente
docker compose up --build -d

# Producción: descarga la imagen publicada por el pipeline
docker compose -f docker-compose.prod.yml up -d
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información de la aplicación |
| GET | `/health` | Estado del servicio |
| GET | `/version` | Versión desplegada |
| GET | `/suma/{a}/{b}` | Operación de ejemplo |
| GET | `/docs` | Documentación Swagger |

## Tests

```bash
cd src
pip install -r requirements.txt pytest httpx
pytest tests/ -v
```

## Secretos requeridos

Configurados en *Settings → Secrets and variables → Actions*:

| Secreto | Descripción |
|---------|-------------|
| `DOCKERHUB_USERNAME` | Docker ID |
| `DOCKERHUB_TOKEN` | Access token con permisos Read & Write |

`GITHUB_TOKEN` lo provee GitHub automáticamente para publicar en GHCR.