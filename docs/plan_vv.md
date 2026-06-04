# Plan de Verificación y Validación (V&V)
## Proyecto: Task Manager — DevOps+V&V

**Versión:** 1.0  
**Fecha:** 2026-06-03  
**Equipo:** DevOps+V&V  

---

## 1. Introducción

### 1.1 Propósito
Este documento define el plan completo de Verificación y Validación (V&V) para el sistema **Task Manager**, una aplicación web REST desarrollada con Python/Flask y desplegada mediante contenedores Docker. El plan establece qué se prueba, cómo se prueba, con qué herramientas y cuáles son los criterios de aceptación.

### 1.2 Alcance
El plan cubre los siguientes componentes:

| Componente | Tecnología | Tipo de V&V |
|---|---|---|
| API REST (backend) | Python 3.13 + Flask 3.0.3 | Unitaria, Funcional, Integración |
| Base de datos | SQLite 3 (WAL mode) | Persistencia, Integridad |
| Infraestructura | Docker, Docker Compose, Nginx | Configuración, Contrato |
| Scripts de automatización | Bash, PowerShell | Estructura, Ejecución |
| Pipeline CI/CD | GitHub Actions | Configuración, Completitud |

### 1.3 Definiciones
- **Verificación:** ¿Construimos el sistema correctamente? (conformidad con especificación)
- **Validación:** ¿Construimos el sistema correcto? (adecuación a requisitos)
- **Caso borde:** Entrada en el límite del dominio válido
- **Caso negativo:** Entrada intencionalmente inválida para verificar manejo de errores

---

## 2. Estrategia de Pruebas

### 2.1 Pirámide de pruebas aplicada

```
         ┌─────────────────┐
         │   E2E / Sistema  │  (Docker healthcheck + smoke test en CI)
         ├─────────────────┤
         │   Integración    │  (test_vv.py: TestVV_Integracion)
         ├─────────────────┤
         │   Funcionales    │  (test_tasks.py + test_vv.py)
         ├─────────────────┤
         │  Configuración   │  (test_infra.py + test_ci.py + test_scripts.py)
         └─────────────────┘
```

### 2.2 Técnicas de diseño de casos de prueba

| Técnica | Aplicación |
|---|---|
| Partición de equivalencia | Grupos: título vacío, título válido, título muy largo |
| Análisis de valores límite | Título 1 char, 1000 chars; descripción 0, 2000 chars |
| Tabla de decisión | Combinaciones de campos en creación/actualización |
| Prueba de transición de estados | pending → in_progress → completed |
| Prueba negativa | Entradas malformadas, tipos incorrectos, rutas inexistentes |
| Inyección de errores | SQL injection, XSS, JSON malformado |

---

## 3. Entorno de Pruebas

### 3.1 Entorno local (pytest)

| Variable | Valor |
|---|---|
| Sistema operativo | Windows 11 / Linux (CI) |
| Python | 3.11, 3.12, 3.13 (matrix en CI) |
| Base de datos | SQLite temporal por test (fixture con tempfile) |
| Framework de pruebas | pytest 8.2.2 + pytest-flask 1.3.0 |
| APP_ENV | test |
| DATABASE_PATH | ruta temporal aislada por sesión |

### 3.2 Entorno CI (GitHub Actions)

| Job | Runner | Python | Propósito |
|---|---|---|---|
| lint | ubuntu-latest | 3.13 | Calidad de código |
| test | ubuntu-latest | 3.11, 3.12, 3.13 | Suite completa |
| docker-build | ubuntu-latest | — | Imagen + healthcheck |
| security | ubuntu-latest | 3.13 | Auditoría de dependencias |

### 3.3 Aislamiento de pruebas
Cada test recibe su propia instancia de la aplicación Flask con una base de datos SQLite temporal, garantizando independencia total entre casos de prueba.

```python
# conftest.py — fixture que garantiza aislamiento
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['DATABASE_PATH'] = db_path
    application = create_app()
    application.config['TESTING'] = True
    yield application
    os.close(db_fd)
    os.unlink(db_path)
```

---

## 4. Casos de Prueba

### 4.1 Módulo: API REST — Funcional básico (test_tasks.py)

| ID | Nombre | Tipo | Entrada | Resultado esperado | Estado |
|---|---|---|---|---|---|
| T-001 | Health check 200 | Funcional | GET /api/health | 200 OK | PASS |
| T-002 | Health body correcto | Funcional | GET /api/health | `{status: ok, service: task-manager}` | PASS |
| T-003 | Lista vacía BD limpia | Funcional | GET /api/tasks | `[]` | PASS |
| T-004 | Lista con tareas creadas | Funcional | POST × 2, GET /api/tasks | 2 tareas | PASS |
| T-005 | Filtro por status=pending | Funcional | GET /api/tasks?status=pending | Solo pending | PASS |
| T-006 | Filtro status inválido | Negativo | GET /api/tasks?status=invalido | 400 | PASS |
| T-007 | Crear tarea retorna 201 | Funcional | POST /api/tasks | 201 Created | PASS |
| T-008 | Crear con todos los campos | Funcional | POST con title, desc, status | Campos correctos | PASS |
| T-009 | Status por defecto pending | Funcional | POST sin status | status=pending | PASS |
| T-010 | Crear sin title → 400 | Negativo | POST sin title | 400 | PASS |
| T-011 | Crear title vacío → 400 | Negativo | POST title="" | 400 | PASS |
| T-012 | Crear status inválido → 400 | Negativo | POST status=malo | 400 | PASS |
| T-013 | Crear sin JSON body → 400 | Negativo | POST sin body | 400 | PASS |
| T-014 | Crear title 500 chars | Borde | POST title=500×'A' | 201 | PASS |
| T-015 | Crear con caracteres especiales | Borde | POST title con `<>'"` | 201, almacenado tal cual | PASS |
| T-016 | Obtener tarea existente | Funcional | GET /api/tasks/{id} | 200, campos correctos | PASS |
| T-017 | Obtener tarea inexistente | Negativo | GET /api/tasks/99999 | 404 | PASS |
| T-018 | Actualizar status | Funcional | PUT con status=completed | 200, status actualizado | PASS |
| T-019 | Actualizar title | Funcional | PUT con nuevo title | 200, title actualizado | PASS |
| T-020 | Actualizar preserva campos | Funcional | PUT solo status | title y desc intactos | PASS |
| T-021 | Actualizar inexistente → 404 | Negativo | PUT /api/tasks/99999 | 404 | PASS |
| T-022 | Actualizar title vacío → 400 | Negativo | PUT title="" | 400 | PASS |
| T-023 | Actualizar status inválido → 400 | Negativo | PUT status=malo | 400 | PASS |
| T-024 | Eliminar tarea existente | Funcional | DELETE /api/tasks/{id} | 200 | PASS |
| T-025 | Tarea eliminada → 404 en GET | Funcional | DELETE + GET | 404 | PASS |
| T-026 | Eliminar inexistente → 404 | Negativo | DELETE /api/tasks/99999 | 404 | PASS |
| T-027 | Doble eliminación → 404 | Negativo | DELETE × 2 mismo id | 2do: 404 | PASS |

### 4.2 Módulo: Infraestructura Docker (test_infra.py)

| ID | Categoría | Pruebas | Estado |
|---|---|---|---|
| I-001→I-013 | Variables de entorno | 3 archivos .env (dev/test/prod): existencia, claves, valores, debug flags, rutas distintas | PASS |
| I-014→I-021 | Dockerfile | Multi-stage, slim, non-root, /data dir, EXPOSE 5000, healthcheck, order deps | PASS |
| I-022→I-035 | docker-compose.yml | 3 servicios app + nginx, perfiles, bind mount dev, sin puertos en prod, healthchecks, volúmenes, red, restart policies | PASS |
| I-036→I-045 | Nginx config | Upstream, proxy headers, security headers, server_tokens off, bloqueo .hidden, access_log off en health | PASS |
| I-046→I-050 | .dockerignore | Excluye .git, tests/, __pycache__, *.db, .env | PASS |

**Total:** 50 pruebas de infraestructura

### 4.3 Módulo: Scripts de automatización (test_scripts.py)

| ID | Categoría | Pruebas | Estado |
|---|---|---|---|
| S-001→S-012 | Existencia | 5 .sh + 5 .ps1 + .flake8 + .gitignore | PASS |
| S-013→S-034 | Estructura Bash | Shebang, set -euo pipefail, comandos clave por script | PASS |
| S-035→S-051 | Estructura PowerShell | ErrorActionPreference, params, comandos por script | PASS |
| S-052→S-060 | Archivos config | .flake8: sección, max-line-length, exclude; .gitignore: venv, pycache, .pyc, .db | PASS |
| S-061→S-064 | Ejecución real | lint.ps1 pasa, test.ps1 sin recursión, healthcheck.ps1 falla sin servidor | PASS |

**Total:** 64 pruebas de scripts

### 4.4 Módulo: Pipeline CI/CD (test_ci.py)

| ID | Categoría | Pruebas | Estado |
|---|---|---|---|
| C-001→C-003 | Existencia | workflows/, ci.yml, docker-publish.yml | PASS |
| C-004→C-005 | Validez YAML | Ambos archivos son YAML válido | PASS |
| C-006→C-031 | Estructura CI | Triggers, jobs, matrix, dependencias, checkout, versiones, concurrencia, artifacts | PASS |
| C-032→C-040 | Publicación Docker | Tags semver, GHCR, GITHUB_TOKEN, metadata, push habilitado, permisos | PASS |
| C-041→C-046 | Consistencia proyecto | Python versions, requirements.txt, app/, .flake8, Dockerfile, cache GHA | PASS |

**Total:** 46 pruebas de CI/CD

### 4.5 Módulo: V&V Ampliado (test_vv.py)

#### VV-F: Funcionales

| ID | Caso de prueba | Estado |
|---|---|---|
| VV-F-01 | Crear tarea con todos los campos simultáneamente | PASS |
| VV-F-02 | Tarea recién creada tiene created_at y updated_at | PASS |
| VV-F-03 | updated_at cambia en actualización | PASS |
| VV-F-04 | created_at NO cambia en actualización | PASS |
| VV-F-05 | Listado ordena más recientes primero | PASS |
| VV-F-06 | Filtro por status=in_progress funciona | PASS |
| VV-F-07 | Filtro por status=completed funciona | PASS |
| VV-F-08 | Filtro no contamina entre estados | PASS |
| VV-F-09 | Actualizar solo description | PASS |
| VV-F-10 | Actualizar múltiples campos simultáneamente | PASS |
| VV-F-11 | DELETE exitoso retorna mensaje de confirmación | PASS |
| VV-F-12 | Tarea creada aparece en listado | PASS |
| VV-F-13 | Tarea eliminada NO aparece en listado | PASS |
| VV-F-14 | Health devuelve service name correcto | PASS |
| VV-F-15 | IDs son únicos y auto-incrementados | PASS |

#### VV-N: Negativos

| ID | Caso de prueba | Estado |
|---|---|---|
| VV-N-01 | Crear sin Content-Type JSON → 400 | PASS |
| VV-N-02 | Crear con title solo espacios → 400 | PASS |
| VV-N-03 | Crear con status=null → no 500 | PASS |
| VV-N-04 | Crear con JSON malformado → 400 | PASS |
| VV-N-05 | Actualizar sin body → 400 | PASS |
| VV-N-06 | Actualizar status inválido → 400 | PASS |
| VV-N-07 | Actualizar title=null → 400 | PASS |
| VV-N-08 | GET id=0 → 404 | PASS |
| VV-N-09 | DELETE id=999999 → 404 | PASS |
| VV-N-10 | Respuesta de error tiene campo 'error' | PASS |
| VV-N-11 | Filtro inválido retorna 400 con mensaje | PASS |
| VV-N-12 | Ruta inexistente → 404 | PASS |

#### VV-B: Borde

| ID | Caso de prueba | Estado |
|---|---|---|
| VV-B-01 | Título de 1 solo carácter | PASS |
| VV-B-02 | Título de 1000 caracteres | PASS |
| VV-B-03 | Descripción vacía aceptada | PASS |
| VV-B-04 | Descripción de 2000 caracteres | PASS |
| VV-B-05 | Título con emojis Unicode | PASS |
| VV-B-06 | Título con caracteres chinos | PASS |
| VV-B-07 | Título con HTML almacenado como texto plano | PASS |
| VV-B-08 | SQL injection en título (parametrizado, no vulnerable) | PASS |
| VV-B-09 | Crear 100 tareas y listarlas todas | PASS |
| VV-B-10 | ID=0 → 404 | PASS |
| VV-B-11 | ID negativo → 404 o 405 | PASS |
| VV-B-12 | Título con solo \t → 400 | PASS |
| VV-B-13 | Título con solo \n → 400 | PASS |
| VV-B-14 | Body JSON vacío {} → 400 | PASS |

#### VV-I: Integración

| ID | Caso de prueba | Estado |
|---|---|---|
| VV-I-01 | Flujo completo CRUD (Crear→Leer→Actualizar→Eliminar) | PASS |
| VV-I-02 | Transición de estados pending→in_progress→completed | PASS |
| VV-I-03 | Modificar tarea A no afecta tarea B | PASS |
| VV-I-04 | Eliminar tarea B no elimina tarea A | PASS |
| VV-I-05 | Cambio de estado se refleja en filtros | PASS |
| VV-I-06 | Actualizar un campo preserva todos los demás | PASS |
| VV-I-07 | Listado vacío tras eliminar todas las tareas propias | PASS |

#### VV-H: HTTP

| ID | Caso de prueba | Estado |
|---|---|---|
| VV-H-01 | Todas las respuestas son Content-Type application/json | PASS |
| VV-H-02 | POST retorna 201 al crear | PASS |
| VV-H-03 | GET retorna 200 en listado | PASS |
| VV-H-04 | PUT retorna 200 en actualización exitosa | PASS |
| VV-H-05 | DELETE retorna 200 en eliminación exitosa | PASS |
| VV-H-06 | Errores 400 incluyen cuerpo JSON con 'error' | PASS |
| VV-H-07 | Errores 404 incluyen cuerpo JSON | PASS |
| VV-H-08 | Respuesta de lista es array JSON | PASS |
| VV-H-09 | Respuesta de tarea individual es objeto JSON | PASS |
| VV-H-10 | Todos los campos obligatorios presentes en respuesta | PASS |

**Total:** 58 pruebas V&V ampliadas

---

## 5. Resumen de Cobertura

| Módulo | Archivo de pruebas | Nro. pruebas | Resultado |
|---|---|---|---|
| API REST (CRUD) | tests/test_tasks.py | 27 | ✅ 27/27 PASS |
| Infraestructura Docker | tests/test_infra.py | 50 | ✅ 50/50 PASS |
| Scripts automatización | tests/test_scripts.py | 64 | ✅ 64/64 PASS |
| Pipeline CI/CD | tests/test_ci.py | 46 | ✅ 46/46 PASS |
| V&V ampliado | tests/test_vv.py | 58 | ✅ 58/58 PASS |
| **TOTAL** | — | **245** | **✅ 245/245 PASS** |

**Tasa de éxito: 100%**

---

## 6. Criterios de Aceptación

### 6.1 Criterios de paso del sistema (Definition of Done)

| Criterio | Requerimiento | Estado |
|---|---|---|
| Todos los tests pasan | 100% PASS sin skips en funcionales | ✅ |
| Sin errores de lint | flake8 app/ → exit code 0 | ✅ |
| Sin vulnerabilidades críticas | pip-audit sin CVE críticas | ✅ |
| Imagen Docker buildea | docker build → exit code 0 | ✅ (CI) |
| Healthcheck pasa en contenedor | /api/health → `{status: ok}` | ✅ (CI) |
| Cobertura de casos negativos | ≥10 casos negativos verificados | ✅ (24 casos) |
| Cobertura de casos borde | ≥5 casos borde verificados | ✅ (14 casos) |

### 6.2 Criterios de fallo (bloqueantes)

- Cualquier test funcional (CRUD) en estado FAIL
- Imagen Docker no puede construirse
- Contenedor Docker no supera healthcheck
- Vulnerabilidad crítica (CVSS ≥ 9.0) en dependencias
- Error 500 en cualquier endpoint documentado

---

## 7. Herramientas y Versiones

| Herramienta | Versión | Uso |
|---|---|---|
| pytest | 8.2.2 | Ejecución de pruebas |
| pytest-flask | 1.3.0 | Cliente Flask para pruebas |
| flake8 | 7.1.0 | Análisis estático de código |
| pyyaml | 6.0.2 | Parseo de archivos YAML en tests |
| pip-audit | latest | Auditoría de vulnerabilidades |
| Docker Buildx | latest | Construcción multi-arquitectura |
| GitHub Actions | — | Ejecución automatizada en CI |

---

## 8. Gestión de Defectos

### 8.1 Defectos encontrados y resueltos durante el desarrollo

| ID | Descripción | Severidad | Estado |
|---|---|---|---|
| BUG-001 | `PUT /api/tasks/<id>` con `{"title": ""}` retornaba 200 en lugar de 400 porque `data.get('title') or row['title']` caía al valor existente cuando se pasaba string vacío. | Alta | ✅ Resuelto: se separó la comprobación `if 'title' in data` de la validación de vaciedad |
| BUG-002 | `GET /api/tasks` sin tiebreaker en `ORDER BY created_at DESC` devolvía orden no determinista cuando dos tareas se creaban en el mismo segundo. | Media | ✅ Resuelto: se agregó `id DESC` como criterio secundario de ordenamiento |
| BUG-003 | Tests de CI fallaban por PyYAML parsear la clave `on` de GitHub Actions como booleano `True`. | Baja | ✅ Resuelto: se usa `ci.get(True, ci.get("on", {}))` en los tests |

---

## 9. Automatización y CI/CD

El pipeline de GitHub Actions (`.github/workflows/ci.yml`) ejecuta automáticamente toda la suite V&V en cada push y pull request:

```
push/PR a main|develop
        │
        ▼
    ┌───────┐
    │ lint  │ flake8 app/
    └───┬───┘
        │
        ▼
    ┌───────────────────────────────────────┐
    │ test (matrix: Python 3.11/3.12/3.13)  │ pytest --tb=short + JUnit XML
    └──────────────────┬────────────────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
    ┌────────────┐         ┌──────────────┐
    │docker-build│         │   security   │
    │healthcheck │         │  pip-audit   │
    └─────┬──────┘         └──────────────┘
          │
          ▼
    ┌────────────┐
    │ ci-summary │ Falla si lint/test/docker fallan
    └────────────┘
```

---

## 10. Validación del Sistema

### 10.1 Verificación: ¿El sistema cumple las especificaciones?

La **verificación** evalúa si el sistema fue construido correctamente según los requisitos técnicos definidos.

| Requisito técnico | Evidencia | Resultado |
|---|---|---|
| API REST con endpoints CRUD | 27 tests T-001..T-027 PASS | ✅ Verificado |
| Estados: pending, in_progress, completed | CHECK constraint en BD + validación API | ✅ Verificado |
| Respuestas JSON con Content-Type correcto | VV-H-01..VV-H-10 PASS | ✅ Verificado |
| Campos obligatorios en respuesta (id, title, description, status, created_at, updated_at) | VV-H-10 PASS | ✅ Verificado |
| Rechazo de entradas inválidas con 400 | VV-N-01..VV-N-12 PASS | ✅ Verificado |
| Comportamiento correcto en límites | VV-B-01..VV-B-14 PASS | ✅ Verificado |
| Aislamiento entre ambientes (dev/test/prod) | I-001..I-013 PASS | ✅ Verificado |
| Imagen Docker multi-stage sin root | I-014..I-021 PASS | ✅ Verificado |
| Pipeline CI con lint + test + docker + security | C-001..C-046 PASS | ✅ Verificado |
| Scripts de automatización con estructura correcta | S-001..S-064 PASS | ✅ Verificado |

**Conclusión de verificación:** El sistema cumple al 100% con las especificaciones técnicas. Los 245 tests cubren todos los requisitos definidos y pasan sin fallos.

### 10.2 Validación: ¿El sistema cumple las necesidades del usuario?

La **validación** evalúa si el sistema fue construido correcto, es decir, si satisface las necesidades reales del negocio/usuario.

| Necesidad del usuario | Implementación | Prueba de validación | Estado |
|---|---|---|---|
| **Crear tareas** con título, descripción y estado | `POST /api/tasks` — retorna 201 con todos los campos | VV-F-01, T-007..T-015 | ✅ Validado |
| **Editar tareas** actualizando uno o varios campos | `PUT /api/tasks/{id}` — actualiza y preserva campos no enviados | VV-F-09, VV-F-10, VV-I-06 | ✅ Validado |
| **Eliminar tareas** y confirmar la eliminación | `DELETE /api/tasks/{id}` — retorna confirmación y 404 en GET posterior | VV-F-11, VV-F-13, VV-I-01 | ✅ Validado |
| **Gestionar estados** (pendiente→en progreso→completado) | Transiciones libres entre cualquier estado válido | VV-I-02, T-018 | ✅ Validado |
| **Filtrar tareas** por estado | `GET /api/tasks?status=X` — devuelve solo las del estado solicitado | VV-F-06, VV-F-07, VV-F-08, VV-I-05 | ✅ Validado |
| **Acceso vía navegador web** | Frontend HTML5/CSS3/JS en `/` + API REST | Frontend integrado en `/` | ✅ Validado |
| **Sistema confiable** (no pierde datos) | Transacciones SQLite con commit explícito; WAL mode | VV-I-03, VV-I-04, VV-B-09 | ✅ Validado |
| **Seguridad básica** (no vulnerable a SQL injection) | Consultas parametrizadas en todos los endpoints | VV-B-08 | ✅ Validado |
| **Despliegue reproducible** entre ambientes | Docker Compose con 3 perfiles y .env por ambiente | test_infra.py PASS | ✅ Validado |
| **Detección temprana de errores** | Pipeline CI automático en cada push | test_ci.py PASS | ✅ Validado |

**Conclusión de validación:** El sistema satisface todas las necesidades de negocio identificadas. El enfoque DevOps+V&V resolvió los problemas originales:

| Problema original | Solución implementada | ¿Resuelto? |
|---|---|---|
| Fallos entre dev y producción | 3 ambientes aislados con .env independientes | ✅ |
| Falta de automatización en despliegues | Scripts + pipeline CI/CD + Docker | ✅ |
| Pruebas manuales poco confiables | 245 tests automatizados con pytest | ✅ |
| Errores detectados tarde | CI ejecuta tests en cada push/PR | ✅ |
| Procesos no reproducibles | Docker Compose + infraestructura como código | ✅ |

---

## 11. Análisis de Errores

### 11.1 Registro completo de errores detectados

| ID | Tipo | Descripción del error | Cuándo se detectó | Quién detectó |
|---|---|---|---|---|
| BUG-001 | Lógica de negocio | `PUT` con `title:""` retornaba 200 silencioso en lugar de 400 | Fase V&V — test T-022 | Suite automatizada |
| BUG-002 | Comportamiento de BD | Orden de listado no determinista con timestamps del mismo segundo | Fase V&V — test VV-F-05 | Suite automatizada |
| BUG-003 | Compatibilidad de herramientas | PyYAML parsea clave YAML `on` como booleano `True` | Fase CI/CD — test C-006 | Suite automatizada |

### 11.2 Análisis de impacto

#### BUG-001 — Actualización silenciosa de título

**Impacto en el usuario:**
- Un cliente de la API creía haber borrado el título de una tarea enviando `{"title": ""}`, pero el servidor conservaba el valor anterior sin notificarlo.
- Violación del principio de "honestidad" de la API: el cliente no podía distinguir si su solicitud fue procesada o ignorada.
- **Nivel de riesgo:** Alto. Podría causar inconsistencias en clientes que construyen lógica sobre la respuesta.

**Impacto en el sistema:**
- No causaba corrupción de datos (los datos quedaban correctos), pero la respuesta 200 confundía al cliente.
- Si se hubiera detectado en producción, hubiera requerido comunicar la corrección a todos los clientes de la API.

**Costo estimado de corrección:**
- En pruebas (detectado): ~5 minutos — un cambio de 8 líneas en `routes.py`
- En producción (estimado): investigación, hotfix, despliegue, comunicación a clientes → ~2-4 horas

#### BUG-002 — Orden no determinista en listado

**Impacto en el usuario:**
- El usuario veía el listado de tareas en un orden diferente en recargas sucesivas cuando dos tareas tenían el mismo timestamp.
- Comportamiento confuso en la UI (las tarjetas "se mueven" sin razón aparente).
- **Nivel de riesgo:** Medio. No causaba pérdida de datos pero afectaba la experiencia de usuario.

**Impacto en el sistema:**
- Los tests que verificaban el orden fallaban intermitentemente (flaky tests), erosionando la confianza en la suite.
- Un test no determinista es peor que no tener test: puede ocultar bugs reales.

**Costo estimado de corrección:**
- En pruebas (detectado): ~2 minutos — agregar `, id DESC` a la query SQL
- En producción (estimado): difícil de reproducir, reportes de usuarios confusos → ~1-3 horas de investigación

#### BUG-003 — Clave YAML `on` parseada como booleano

**Impacto en el usuario:**
- Solo afectaba a los tests, no a la aplicación ni al pipeline real de GitHub Actions.
- Los tests del módulo CI/CD fallaban aunque la configuración era correcta.
- **Nivel de riesgo:** Bajo. No afectaba funcionalidad de producción.

**Impacto en el sistema:**
- 15 tests del módulo `test_ci.py` fallaban con `KeyError: 'on'`.
- Reducía la confianza en la validación del CI.

**Costo estimado de corrección:**
- En pruebas (detectado): ~10 minutos — ajustar acceso con `ci.get(True, ci.get("on", {}))`
- Sin tests: podría haber pasado desapercibido durante semanas si se asumía que el CI era correcto

### 11.3 Mejoras propuestas

#### Mejoras inmediatas (Prioridad Alta)

| ID | Mejora | Motivación | Esfuerzo |
|---|---|---|---|
| M-001 | Añadir validación de longitud máxima de título (≤ 500 chars) y descripción (≤ 5000 chars) | Prevenir datos excesivamente grandes que degraden la BD | 30 min |
| M-002 | Timestamps con precisión de milisegundos: `strftime('%Y-%m-%dT%H:%M:%f', 'now')` | Eliminar definitivamente el riesgo de BUG-002 en futuras pruebas | 1 hora |
| M-003 | Paginación en `GET /api/tasks` con `?page=1&per_page=20` | Evitar degradación de rendimiento con cientos de tareas | 2 horas |

#### Mejoras a medio plazo (Prioridad Media)

| ID | Mejora | Motivación | Esfuerzo |
|---|---|---|---|
| M-004 | Autenticación JWT para proteger endpoints | Sin auth, cualquier usuario puede borrar tareas de otros | 1 día |
| M-005 | Migrar a PostgreSQL en producción | SQLite no es adecuado para múltiples usuarios concurrentes | 2 días |
| M-006 | Añadir cobertura de código con `coverage.py` + umbral mínimo 80% | Visibilidad de código no probado | 2 horas |
| M-007 | Tests de performance con locust | Validar que la API responde en < 200ms bajo carga | 4 horas |

#### Mejoras de proceso (Prioridad Media)

| ID | Mejora | Motivación | Esfuerzo |
|---|---|---|---|
| M-008 | Branch protection: requerir CI verde para merge a main | Prevenir introducción de regresiones | 15 min (config GitHub) |
| M-009 | Análisis estático de seguridad con bandit | Detectar patrones inseguros en Python (ej. uso de `eval`) | 1 hora |
| M-010 | Notificaciones automáticas al equipo cuando CI falla | Feedback inmediato, sin revisar manualmente GitHub | 30 min |

### 11.4 Lecciones aprendidas del análisis de errores

1. **El 100% de los bugs fue detectado por tests automatizados antes de llegar a producción.** Esto demuestra el ROI directo de invertir en una suite de pruebas completa.

2. **Los bugs encontrados tienen mayor impacto en producción que en desarrollo.** El costo de corregir BUG-001 en producción hubiera sido ~30x mayor que el costo real de corrección en pruebas.

3. **Los tests no deterministas (flaky tests) son un bug en sí mismos.** BUG-002 producía un test que a veces pasaba y a veces fallaba, lo cual es tan dañino como no tener test: erosiona la confianza en la suite completa.

4. **Conocer las herramientas en profundidad evita debugging innecesario.** BUG-003 (PyYAML y booleanos) era un problema conocido de YAML 1.1 que se hubiera podido prevenir con documentación adecuada en el equipo.
