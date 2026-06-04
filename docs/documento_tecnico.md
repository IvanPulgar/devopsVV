# Documento Técnico
## Sistema Task Manager — Proyecto Integrador DevOps + V&V

**Versión:** 1.0  
**Fecha:** 2026-06-03  
**Asignatura:** DevOps + Verificación y Validación  

---

## 1. Descripción del Sistema

### 1.1 Contexto y problema

Una empresa tecnológica necesita una herramienta de gestión de tareas para sus equipos de trabajo. El equipo de desarrollo enfrentaba los siguientes problemas:

| Problema | Impacto |
|---|---|
| Fallos entre ambientes dev y producción | Errores en producción no detectados antes del despliegue |
| Despliegues manuales sin procedimiento definido | Inconsistencia y riesgo de regresión |
| Pruebas manuales poco confiables | Errores detectados tarde, mayor costo de corrección |
| Entornos no reproducibles | "Funciona en mi máquina" — imposible de auditar |
| Sin análisis estático del código | Deuda técnica acumulada sin control |

### 1.2 Solución propuesta

Se diseñó e implementó el sistema **Task Manager** con una metodología DevOps completa que integra:

- **Gestión de ambientes:** tres entornos aislados (dev/test/prod) con variables de entorno independientes
- **Infraestructura como código:** Docker multi-stage + Docker Compose + Nginx como reverse proxy
- **Automatización total:** scripts para instalación, ejecución, pruebas, lint y health-check
- **Integración continua:** pipeline GitHub Actions de 5 etapas que corre en cada push
- **V&V:** 245 pruebas automatizadas que cubren funcionalidad, límites, negativos e integración

### 1.3 Funcionalidades del sistema

El Task Manager permite:

| Funcionalidad | Endpoint | Método |
|---|---|---|
| Listar todas las tareas | `/api/tasks` | GET |
| Listar tareas filtradas por estado | `/api/tasks?status=pending` | GET |
| Crear una tarea | `/api/tasks` | POST |
| Obtener una tarea específica | `/api/tasks/{id}` | GET |
| Actualizar una tarea | `/api/tasks/{id}` | PUT |
| Eliminar una tarea | `/api/tasks/{id}` | DELETE |
| Verificar estado del servicio | `/api/health` | GET |

**Estados de tarea soportados:**

```
pending  →  in_progress  →  completed
```

Las transiciones son libres: cualquier estado puede pasar a cualquier otro, permitiendo flujos de trabajo flexibles.

### 1.4 Stack tecnológico

| Capa | Tecnología | Versión |
|---|---|---|
| Backend | Python + Flask | 3.13 / 3.0.3 |
| Base de datos | SQLite (WAL mode) | 3 |
| Frontend | HTML5 + CSS3 + JavaScript | vanilla |
| Reverse proxy | Nginx | 1.27-alpine |
| Contenedores | Docker + Docker Compose | multi-stage |
| CI/CD | GitHub Actions | v4 |
| Pruebas | pytest + pytest-flask | 8.2.2 / 1.3.0 |
| Análisis estático | flake8 | 7.1.0 |
| Auditoría de seguridad | pip-audit | latest |

---

## 2. Arquitectura General

### 2.1 Diagrama de capas

```
┌──────────────────────────────────────────────────────┐
│                   CLIENTE (Navegador)                │
│              HTML5 / CSS3 / JavaScript               │
└────────────────────────┬─────────────────────────────┘
                         │ HTTP
                         ▼
┌──────────────────────────────────────────────────────┐
│              NGINX (Reverse Proxy)                   │
│   Puerto 80 → Upstream app_prod:5000                 │
│   Headers de seguridad + rate limiting               │
└────────────────────────┬─────────────────────────────┘
                         │ HTTP interno
                         ▼
┌──────────────────────────────────────────────────────┐
│             FLASK APPLICATION (Python)               │
│                                                      │
│  ┌──────────────┐    ┌─────────────────────────┐     │
│  │  app.py      │    │  routes.py (Blueprint)  │     │
│  │  create_app()│───►│  /api/health            │     │
│  │  init_db()   │    │  /api/tasks  (CRUD)     │     │
│  └──────────────┘    └───────────┬─────────────┘     │
│                                  │                   │
│  ┌───────────────────────────────┴──────────────┐    │
│  │            database.py                       │    │
│  │  get_db() — conexión SQLite con WAL + FK     │    │
│  └───────────────────────────────┬──────────────┘    │
└──────────────────────────────────┼───────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   SQLite DB       │
                         │  taskmanager.db   │
                         │  (volumen /data)  │
                         └───────────────────┘
```

### 2.2 Modelo de datos

La base de datos contiene una única tabla `tasks`:

```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    status      TEXT    NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'in_progress', 'completed')),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

**Restricciones implementadas a nivel de BD:**
- `NOT NULL` en `title` y `status`
- Constraint `CHECK` que valida los tres estados permitidos
- Timestamps automáticos con `datetime('now')` de SQLite

**Restricciones adicionales a nivel de API (routes.py):**
- Validación de título no vacío después de strip (previene títulos de solo espacios/tabs)
- Validación de estado antes de INSERT/UPDATE
- Consultas parametrizadas (prevención de SQL injection)
- WAL mode habilitado para mejor concurrencia de lecturas

### 2.3 Patrón de diseño: Application Factory

Se usa el patrón `create_app()` de Flask para:
- Separar configuración de la creación de la app
- Facilitar tests con apps independientes
- Soportar múltiples instancias con configuraciones distintas

```python
# app/app.py
def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(tasks_bp)
    return app
```

---

## 3. Gestión de Ambientes

### 3.1 Tres ambientes definidos

El proyecto implementa tres ambientes completamente aislados, cada uno con su propia configuración:

| Parámetro | Development | Test | Production |
|---|---|---|---|
| Archivo config | `.env.dev` | `.env.test` | `.env.prod` |
| DEBUG | `True` | `False` | `False` |
| DATABASE_PATH | `/data/dev.db` | `/data/test.db` | `/data/prod.db` |
| Puerto externo | 5000 | 5001 | 80 (via Nginx) |
| Nginx | No | No | Sí |
| Hot-reload | Sí (bind-mount) | No | No |
| Perfil Docker | `dev` | `test` | `prod` |

### 3.2 Activación de ambientes con Docker Compose

```bash
# Ambiente de desarrollo (hot-reload, puerto 5000)
docker compose --profile dev up

# Ambiente de pruebas (aislado, puerto 5001)
docker compose --profile test up

# Ambiente de producción (Nginx + app, puerto 80)
docker compose --profile prod up
```

### 3.3 Variables de entorno

Cada ambiente usa variables independientes que controlan el comportamiento completo de la app:

```bash
# .env.dev (ejemplo)
FLASK_ENV=development
APP_ENV=dev
DEBUG=True
HOST=0.0.0.0
PORT=5000
DATABASE_PATH=/data/dev.db

# .env.prod (ejemplo)
FLASK_ENV=production
APP_ENV=prod
DEBUG=False
HOST=0.0.0.0
PORT=5000
DATABASE_PATH=/data/prod.db
```

El archivo `.env.example` documenta todas las variables disponibles. El `.gitignore` excluye los archivos `.env.*` del repositorio por seguridad.

### 3.4 Diferencias clave entre ambientes

**Development:**
- Código montado como bind-mount para detectar cambios sin rebuild
- Debug habilitado con Werkzeug reloader
- Base de datos separada en `/data/dev.db`

**Test:**
- Tests ejecutan con BD temporal (`tempfile.mkstemp`) — completamente efímera
- Sin puertos expuestos en producción durante tests
- Fixture de pytest destruye la BD al terminar cada test

**Production:**
- Nginx como reverse proxy con headers de seguridad (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`)
- `server_tokens off` para no exponer versión de Nginx
- Usuario no-root (`appuser`) en el contenedor
- Imagen multi-stage: builder (instala deps) → runtime (solo código necesario)

---

## 4. Flujo DevOps

### 4.1 Pipeline de integración continua (CI)

El pipeline está implementado en `.github/workflows/ci.yml` y se ejecuta automáticamente en cada push a `main`/`develop` y en pull requests:

```
push a main/develop o PR
         │
         ▼
  ┌────────────┐
  │  1. lint   │  flake8 app/ — max-line-length=120
  └─────┬──────┘    Si falla → pipeline detenido
        │
        ▼
  ┌─────────────────────────────────────────┐
  │  2. test  (matrix: 3.11 / 3.12 / 3.13) │  pytest 245 tests + JUnit XML
  └────────────────┬────────────────────────┘    Si alguno falla → pipeline detenido
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
  ┌───────────┐       ┌─────────────┐
  │ 3. docker │       │ 4. security │
  │   build   │       │  pip-audit  │
  │ + smoke   │       │  (CVEs)     │
  └─────┬─────┘       └──────┬──────┘
        │                    │
        └─────────┬──────────┘
                  ▼
           ┌────────────┐
           │ 5. summary │  Falla si lint/test/docker fallaron
           └────────────┘
```

**Características del pipeline:**
- **Concurrencia:** cancela ejecuciones anteriores del mismo branch/PR
- **Cache:** caché de dependencias pip para acelerar builds
- **Artefactos:** upload de JUnit XML para visualización de resultados en GitHub
- **Smoke test:** tras build Docker, levanta el contenedor y hace `curl /api/health`

### 4.2 Scripts de automatización

Se proporcionan scripts equivalentes para Linux (Bash) y Windows (PowerShell):

| Script | Propósito | Bash | PowerShell |
|---|---|---|---|
| install | Crea venv e instala dependencias | `scripts/install.sh` | `scripts/install.ps1` |
| run | Arranca la aplicación en un ambiente | `scripts/run.sh` | `scripts/run.ps1` |
| test | Ejecuta la suite de pruebas | `scripts/test.sh` | `scripts/test.ps1` |
| lint | Corre flake8 sobre `app/` | `scripts/lint.sh` | `scripts/lint.ps1` |
| healthcheck | Verifica si el servidor responde | `scripts/healthcheck.sh` | `scripts/healthcheck.ps1` |

**Características de todos los scripts Bash:**
```bash
#!/usr/bin/env bash
set -euo pipefail  # falla ante cualquier error, variable sin definir o pipe fallido
```

**Ejemplo de uso:**
```bash
# Linux/macOS
./scripts/install.sh
./scripts/run.sh dev
./scripts/test.sh

# Windows PowerShell
.\scripts\install.ps1
.\scripts\run.ps1 -Env dev
.\scripts\test.ps1
```

### 4.3 Proceso de entrega continua (CD)

El workflow `.github/workflows/docker-publish.yml` automatiza la publicación de la imagen Docker:

**Trigger:** tags con formato `v*.*.*` (por ejemplo `v1.0.0`)

```
git tag v1.0.0
git push origin v1.0.0
         │
         ▼
  docker build (multi-arch)
         │
         ▼
  docker push → ghcr.io/<owner>/task-manager:1.0.0
                ghcr.io/<owner>/task-manager:latest
```

**Características:**
- Autenticación con `GITHUB_TOKEN` (sin secretos adicionales)
- Metadata automática de imagen (labels OCI)
- Caché de capas entre builds

### 4.4 Infraestructura como código

```
devopsVV/
├── Dockerfile              # Multi-stage: builder → runtime
├── docker-compose.yml      # 3 servicios, 3 perfiles, healthchecks
├── infra/
│   └── nginx/
│       ├── nginx.conf                    # Configuración global Nginx
│       └── conf.d/taskmanager.conf       # Virtual host con proxy y headers
└── .github/
    └── workflows/
        ├── ci.yml                        # Pipeline CI (5 jobs)
        └── docker-publish.yml            # CD: publica imagen en GHCR
```

---

## 5. Estrategia de Pruebas

### 5.1 Organización de la suite

La suite de pruebas tiene **245 casos** organizados en 5 módulos:

| Módulo | Archivo | Tests | Objetivo |
|---|---|---|---|
| API CRUD | `tests/test_tasks.py` | 27 | Verificar todos los endpoints REST |
| Infraestructura | `tests/test_infra.py` | 50 | Validar Docker, Nginx, .env |
| Scripts | `tests/test_scripts.py` | 64 | Estructura y ejecución de scripts |
| CI/CD | `tests/test_ci.py` | 46 | Configuración del pipeline |
| V&V ampliado | `tests/test_vv.py` | 58 | Funcional, negativo, borde, HTTP |
| **Total** | | **245** | |

### 5.2 Tipos de prueba implementados

**Funcionales (VV-F):** Verifican que las funcionalidades definidas operan correctamente: timestamps, ordenamiento, filtros, CRUD completo.

**Negativos (VV-N):** Verifican que el sistema rechaza correctamente entradas inválidas: JSON malformado, titles vacíos, estados inexistentes, rutas no definidas.

**Borde (VV-B):** Verifican comportamiento en límites del dominio: 1 carácter, 1000 caracteres, Unicode, emojis, SQL injection, cuerpo vacío.

**Integración (VV-I):** Verifican flujos encadenados: CRUD completo, transiciones de estado, independencia entre tareas.

**HTTP (VV-H):** Verifican conformidad del protocolo: Content-Type, códigos de estado, forma de los JSON de respuesta.

**Configuración:** Verifican que todos los archivos de infraestructura tienen la estructura correcta (Dockerfile, docker-compose.yml, Nginx, scripts, CI).

### 5.3 Aislamiento de pruebas

Cada test recibe una base de datos SQLite temporal creada con `tempfile.mkstemp()` y destruida al finalizar, garantizando independencia total entre casos.

### 5.4 Ejecución de la suite

```bash
# Ejecutar suite completa
py -m pytest --tb=short -v

# Ejecutar solo el módulo V&V
py -m pytest tests/test_vv.py -v

# Ejecutar con filtro por nombre
py -m pytest -k "negativo" -v
```

---

## 6. Resultados Obtenidos

### 6.1 Resultados de la suite de pruebas

Ejecución del `2026-06-03` sobre Python 3.13.6 en Windows 11:

```
============================= test session starts =============================
platform win32 -- Python 3.13.6, pytest-8.2.2, pluggy-1.6.0
collected 245 items

tests/test_ci.py          ...........................    46 passed
tests/test_infra.py       ..................................................    50 passed
tests/test_scripts.py     ..................................................    64 passed
tests/test_tasks.py       ...........................    27 passed
tests/test_vv.py          ..................................................    58 passed

========================== 245 passed in ~12s =================================
```

**Tasa de éxito: 100% — 245/245 tests PASS**

### 6.2 Resultados de análisis estático

```bash
$ py -m flake8 app/
# Sin salida → 0 errores, 0 advertencias
# Exit code: 0
```

### 6.3 Cobertura por tipo de prueba

| Tipo | Cantidad | Resultado |
|---|---|---|
| Funcionales | 42 | ✅ 100% PASS |
| Negativos | 36 | ✅ 100% PASS |
| Borde | 19 | ✅ 100% PASS |
| Integración | 14 | ✅ 100% PASS |
| HTTP | 10 | ✅ 100% PASS |
| Configuración/Infra | 124 | ✅ 100% PASS |

### 6.4 Validación por requisito de negocio

| Requisito | Prueba(s) | Estado |
|---|---|---|
| Crear tareas | T-007..T-015, VV-F-01 | ✅ Verificado |
| Editar tareas | T-018..T-023, VV-F-09/10 | ✅ Verificado |
| Eliminar tareas | T-024..T-027, VV-F-11 | ✅ Verificado |
| Gestionar estados | T-018, VV-I-02 | ✅ Verificado |
| Accesible vía web | Frontend HTML5 + `/` | ✅ Verificado |
| Despliegue en entorno cloud | docker-publish.yml → GHCR | ✅ Verificado |
| Tres ambientes aislados | test_infra.py (I-001..I-013) | ✅ Verificado |
| Pipeline CI | test_ci.py (C-001..C-046) | ✅ Verificado |

---

## 7. Problemas Encontrados y Mejoras

### 7.1 Problemas detectados durante el desarrollo

#### BUG-001 — Actualización con título vacío retornaba 200 (Alta severidad)

**Descripción:** `PUT /api/tasks/{id}` con body `{"title": ""}` devolvía HTTP 200 y conservaba el título anterior en lugar de retornar 400.

**Causa raíz:** La lógica `data.get('title') or row['title']` usaba el valor existente como fallback cuando `title` era string vacío, porque en Python `"" or "valor"` evalúa a `"valor"`.

**Impacto:** Un cliente podría creer que actualizó el título a vacío, cuando en realidad el servidor ignoró silenciosamente el cambio. Violación del principio de honestidad de la API.

**Solución implementada:**
```python
# Antes (incorrecto)
title = data.get('title') or row['title']

# Después (correcto)
if 'title' in data:
    title = (data['title'] or '').strip()
    if not title:
        return jsonify({'error': 'El título no puede estar vacío'}), 400
else:
    title = row['title']
```

**Mejora propuesta:** Añadir validación de longitud máxima (ej. 500 caracteres) para prevenir entradas excesivamente largas.

---

#### BUG-002 — Orden no determinista en listado con timestamps iguales (Media severidad)

**Descripción:** `GET /api/tasks` con `ORDER BY created_at DESC` devolvía un orden diferente cuando dos tareas se creaban en el mismo segundo (la prueba VV-F-05 fallaba intermitentemente).

**Causa raíz:** SQLite almacena timestamps con precisión de segundos. Crear dos tareas consecutivas en el mismo segundo produce timestamps idénticos, y SQLite no garantiza orden entre filas con valores iguales.

**Impacto:** Tests no deterministas, posible confusión para usuarios al ver el listado reordenarse entre recargas.

**Solución implementada:**
```sql
-- Antes
ORDER BY created_at DESC

-- Después
ORDER BY created_at DESC, id DESC
```

**Mejora propuesta:** Migrar los timestamps a millisegundos (`strftime('%Y-%m-%dT%H:%M:%f', 'now')`) para mayor precisión y compatibilidad con clientes JavaScript.

---

#### BUG-003 — PyYAML parsea la clave `on:` de GitHub Actions como booleano `True` (Baja severidad)

**Descripción:** Al parsear el archivo `ci.yml` con PyYAML, la clave `on:` (que en YAML sin comillas se interpreta como el booleano `True`) hacía que los tests fallaran al intentar acceder a `ci['on']`.

**Causa raíz:** YAML 1.1 (implementado por PyYAML) interpreta `on`, `off`, `yes`, `no` como booleanos. GitHub Actions los usa como strings.

**Impacto:** Tests de validación del CI fallaban aunque el archivo `ci.yml` era perfectamente válido.

**Solución implementada:**
```python
# Acceso defensivo que maneja ambas representaciones
triggers = ci.get(True, ci.get("on", {}))
```

**Mejora propuesta:** Migrar a `ruamel.yaml` que respeta YAML 1.2 donde `on` es un string. O usar comillas en los archivos CI: `"on":`.

---

### 7.2 Análisis de impacto

| ID | Severidad | Detectado por | Momento detección | Costo corrección |
|---|---|---|---|---|
| BUG-001 | Alta | Test T-022 (suite V&V) | Ejecución local | Bajo (1 cambio en routes.py) |
| BUG-002 | Media | Test VV-F-05 | Ejecución local | Bajo (1 línea SQL) |
| BUG-003 | Baja | Test C-006 | Ejecución local | Bajo (1 línea Python) |

**Conclusión de análisis:** Los tres errores fueron detectados por la suite automatizada antes de llegar a producción. Esto demuestra el valor de tener pruebas automatizadas: el costo de corrección en fase de pruebas es significativamente menor que corregir en producción.

### 7.3 Mejoras propuestas

#### Mejoras técnicas

| Mejora | Prioridad | Complejidad |
|---|---|---|
| Timestamps en millisegundos para mayor precisión | Media | Baja |
| Paginación en `GET /api/tasks` para grandes volúmenes | Alta | Media |
| Autenticación JWT para proteger los endpoints | Alta | Alta |
| Validación de longitud máxima de campos | Media | Baja |
| Migrar de SQLite a PostgreSQL para producción real | Alta | Alta |
| Tests de performance / carga (locust) | Media | Media |

#### Mejoras de proceso

| Mejora | Beneficio |
|---|---|
| Branch protection rules en GitHub | Previene push directo a main sin CI verde |
| Cobertura de código con coverage.py + codecov | Visibilidad de partes no probadas |
| Análisis de seguridad con bandit | Detección de patrones inseguros en Python |
| Notificaciones Slack/Teams en CI | Feedback inmediato al equipo |
| Revisión de código obligatoria (PR review) | Segunda opinión antes de merge |

### 7.4 Lecciones aprendidas

1. **Las pruebas automatizadas pagan desde el primer bug detectado.** Los tres bugs encontrados se corrigieron en minutos gracias a los tests; sin ellos, podrían haber llegado a producción.

2. **El aislamiento de entornos es crítico.** Usar bases de datos temporales por test eliminó completamente la interferencia entre casos de prueba.

3. **Las herramientas multiplataforma requieren atención.** Los scripts Bash/PowerShell deben mantenerse sincronizados. Codificaciones de caracteres (ASCII vs UTF-8) pueden romper scripts en Windows si no se manejan explícitamente.

4. **YAML tiene trampas.** PyYAML (YAML 1.1) interpreta `on` como booleano; conocer las diferencias entre versiones de estándares evita horas de debugging.

5. **La infraestructura como código se prueba igual que el software.** Los 160 tests de infra/scripts/CI aportaron la misma confianza que los tests de negocio.

6. **DevOps es un proceso continuo, no un destino.** La suite actual es sólida, pero las mejoras propuestas (paginación, auth, performance) representan el siguiente ciclo de evolución.
