# Flujo de trabajo Git del taller

## Estrategia de ramas

| Rama | Propósito |
|------|-----------|
| `main` | Documentación general, README, guías |
| `escenario-1-wordpress` | Desarrollo del Escenario 1 |
| `escenario-2-api-node` | Desarrollo del Escenario 2 |
| `escenario-3-redis` | Desarrollo del Escenario 3 |
| `escenario-4-cicd` | Desarrollo del Escenario 4 |

## Ciclo por escenario

```bash
# 1. Partir siempre de main actualizado
git checkout main
git pull origin main

# 2. Crear la rama del escenario
git checkout -b escenario-1-wordpress

# 3. Trabajar y hacer commits frecuentes
git add .
git commit -m "feat: agrega docker-compose para WordPress + MySQL"

# 4. Subir la rama
git push -u origin escenario-1-wordpress

# 5. Al terminar, integrar a main
git checkout main
git merge escenario-1-wordpress
git push origin main
```

## Convención de commits

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un error |
| `docs` | Documentación |
| `style` | Formato, sin cambios de lógica |
| `refactor` | Reestructuración de código |
| `test` | Pruebas |
| `chore` | Configuración y mantenimiento |

Ejemplos:
feat: agrega soporte para phpMyAdmin en escenario 1
fix: corrige conexión a PostgreSQL en escenario 2
docs: actualiza README con instrucciones de uso

## Comandos de consulta frecuentes

```bash
git status                  # Estado del directorio de trabajo
git log --oneline --graph   # Historial resumido
git branch -a               # Todas las ramas, locales y remotas
git diff                    # Cambios aún sin preparar
```