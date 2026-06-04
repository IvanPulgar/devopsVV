# Task Manager — Proyecto Integrador DevOps + V&V

Sistema de gestión de tareas desarrollado con Python/Flask, desplegado mediante Docker y validado con una suite completa de 245 pruebas automatizadas.

## Estado del proyecto

![Tests](https://img.shields.io/badge/tests-245%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![Docker](https://img.shields.io/badge/docker-multi--stage-blue)

---

## Inicio rápido

### Requisitos previos
- Python 3.11+ y `pip`
- Docker y Docker Compose (para despliegue en contenedor)

### Ejecutar en local (sin Docker)

```bash
# 1. Instalar dependencias
./scripts/install.sh          # Linux/macOS
.\scripts\install.ps1         # Windows PowerShell

# 2. Arrancar la aplicación (ambiente dev)
./scripts/run.sh dev
.\scripts\run.ps1 -Env dev

# 3. Abrir en navegador
http://localhost:5000
```

### Ejecutar con Docker

```bash
# Ambiente desarrollo
docker compose --profile dev up

# Ambiente producción (con Nginx en puerto 80)
docker compose --profile prod up
```

---

## Pruebas

```bash
# Suite completa (245 tests)
./scripts/test.sh             # Linux/macOS
.\scripts\test.ps1            # Windows PowerShell

# Solo módulo V&V
py -m pytest tests/test_vv.py -v

# Análisis estático de código
./scripts/lint.sh
```

**Resultado actual:** ✅ 245/245 PASS

| Módulo | Tests |
|---|---|
| API REST (CRUD) | 27 |
| Infraestructura Docker | 50 |
| Scripts de automatización | 64 |
| Pipeline CI/CD | 46 |
| V&V ampliado | 58 |
| **Total** | **245** |

---

## Estructura del proyecto

```
devopsVV/
├── app/                        # Código fuente Flask
│   ├── app.py                  # Application factory (create_app)
│   ├── routes.py               # Endpoints REST (Blueprint)
│   ├── database.py             # Conexión SQLite + init_db()
│   ├── templates/index.html    # Frontend HTML5
│   └── static/                 # CSS y JavaScript
├── tests/                      # Suite de pruebas
│   ├── conftest.py             # Fixtures pytest
│   ├── test_tasks.py           # Tests API CRUD (27)
│   ├── test_infra.py           # Tests infraestructura (50)
│   ├── test_scripts.py         # Tests scripts (64)
│   ├── test_ci.py              # Tests CI/CD (46)
│   └── test_vv.py              # Tests V&V ampliados (58)
├── scripts/                    # Automatización
│   ├── install.sh / install.ps1
│   ├── run.sh / run.ps1
│   ├── test.sh / test.ps1
│   ├── lint.sh / lint.ps1
│   └── healthcheck.sh / healthcheck.ps1
├── infra/nginx/                # Configuración Nginx (producción)
├── docs/
│   ├── documento_tecnico.md    # Documento técnico (7 secciones)
│   └── plan_vv.md              # Plan V&V completo (11 secciones)
├── .github/workflows/
│   ├── ci.yml                  # Pipeline CI (5 jobs)
│   └── docker-publish.yml      # CD: publicación en GHCR
├── Dockerfile                  # Multi-stage: builder → runtime
├── docker-compose.yml          # 3 perfiles: dev / test / prod
├── .env.dev / .env.test / .env.prod
├── .flake8                     # Configuración linter
├── requirements.txt
└── run.py                      # Punto de entrada
```

---

## API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/health` | Estado del servicio |
| GET | `/api/tasks` | Listar tareas (opcional: `?status=pending`) |
| POST | `/api/tasks` | Crear tarea |
| GET | `/api/tasks/{id}` | Obtener tarea |
| PUT | `/api/tasks/{id}` | Actualizar tarea |
| DELETE | `/api/tasks/{id}` | Eliminar tarea |

**Estados válidos:** `pending` | `in_progress` | `completed`

**Ejemplo:**
```bash
# Crear tarea
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Mi tarea", "description": "Descripción", "status": "pending"}'

# Actualizar estado
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

## Ambientes

| Ambiente | Comando | Puerto | Debug |
|---|---|---|---|
| Development | `docker compose --profile dev up` | 5000 | On |
| Test | `docker compose --profile test up` | 5001 | Off |
| Production | `docker compose --profile prod up` | 80 (Nginx) | Off |

---

## Pipeline CI/CD

El pipeline `.github/workflows/ci.yml` ejecuta automáticamente en cada push:

1. **Lint** — flake8 sobre `app/`
2. **Test** — pytest 245 tests en Python 3.11, 3.12 y 3.13 (matrix)
3. **Docker build** — construye la imagen y ejecuta smoke test
4. **Security** — auditoría de dependencias con pip-audit
5. **Summary** — falla si algún job previo falló

---

## Documentación

- [Documento técnico](docs/documento_tecnico.md) — Arquitectura, ambientes, flujo DevOps, resultados, problemas y mejoras
- [Plan V&V](docs/plan_vv.md) — Estrategia de pruebas, catálogo de 245 casos, validación del sistema, análisis de errores
