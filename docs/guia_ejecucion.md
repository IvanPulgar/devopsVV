# Guía de Ejecución — Task Manager
## Proyecto Integrador DevOps + V&V

**Versión:** 1.0
**Fecha:** 2026-06-08
**Propósito:** Guía paso a paso para instalar, ejecutar y probar la aplicación Task Manager desde cero.

---

## Contenido

1. Requisitos previos
2. Instalación y ejecución en LOCAL (Windows)
3. Instalación y ejecución con DOCKER
4. Instalación y ejecución en GITHUB CODESPACES
5. Ejecución de las 245 pruebas — todos los comandos
6. Cómo evidenciar y documentar los resultados

---

## 1. Requisitos Previos

### 1.1 Para ejecución LOCAL (Windows)

Instalar los siguientes programas antes de continuar:

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Python | 3.11 o superior | https://www.python.org/downloads/ |
| Git | cualquiera | https://git-scm.com/download/win |
| Visual Studio Code (opcional) | cualquiera | https://code.visualstudio.com/ |

**Verificar instalaciones:**

```cmd
python --version
git --version
```

Si `python` no funciona, usar el launcher de Windows:

```cmd
C:\Users\<TuUsuario>\AppData\Local\Programs\Python\Launcher\py.exe --version
```

---

### 1.2 Para ejecución con DOCKER

| Herramienta | Descarga |
|---|---|
| Docker Desktop | https://www.docker.com/products/docker-desktop/ |

**Verificar:**

```cmd
docker --version
docker compose version
```

---

### 1.3 Para GITHUB CODESPACES

Solo necesitas:
- Cuenta en https://github.com
- Navegador web (Chrome, Edge, Firefox)

No se requiere instalar nada en tu computadora.

---

## 2. Instalación y Ejecución en LOCAL (Windows)

### Paso 1 — Obtener el código fuente

**Opción A — Clonar desde GitHub (si el repo está en GitHub):**

```cmd
git clone https://github.com/IvanPulgar/devopsVV.git
cd devopsVV
```

**Opción B — Ir directamente a la carpeta local:**

```cmd
cd c:\Users\Hp\Desktop\devopsVV
```

---

### Paso 2 — Crear el entorno virtual e instalar dependencias

```cmd
:: Crear entorno virtual
py -m venv .venv

:: Activar el entorno virtual
.venv\Scripts\activate

:: Verificar que el entorno está activo (debe aparecer (.venv) al inicio del prompt)
:: Instalar todas las dependencias
pip install -r requirements.txt
```

Paquetes que se instalarán:

| Paquete | Versión | Para qué se usa |
|---|---|---|
| flask | 3.0.3 | Framework web del backend |
| python-dotenv | 1.0.1 | Leer variables de entorno desde .env |
| pytest | 8.2.2 | Framework de pruebas |
| pytest-flask | 1.3.0 | Integración de pytest con Flask |
| pyyaml | 6.0.2 | Parseo de archivos YAML en tests |
| flake8 | 7.1.0 | Análisis estático de código |

---

### Paso 3 — Configurar variables de entorno

```cmd
:: Configurar para ambiente desarrollo
set DATABASE_PATH=taskmanager_dev.db
set APP_ENV=development
set DEBUG=true
set PORT=5000
set HOST=0.0.0.0
```

---

### Paso 4 — Levantar la aplicación

```cmd
py run.py
```

**Salida esperada:**

```
  Task Manager corriendo en http://0.0.0.0:5000
  Ambiente: development
 * Serving Flask app 'app.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

### Paso 5 — Verificar que funciona

Abrir el navegador en: **http://localhost:5000**

O verificar la API desde otra terminal:

```cmd
curl http://localhost:5000/api/health
```

**Respuesta esperada:**

```json
{"service": "task-manager", "status": "ok"}
```

---

### Paso 6 — Usar el script automático (alternativa más sencilla)

```powershell
:: Instalar con script
.\scripts\install.ps1

:: Levantar en modo dev
.\scripts\run.ps1 -Env dev

:: Verificar que está corriendo
.\scripts\healthcheck.ps1
```

---

## 3. Instalación y Ejecución con DOCKER

### Paso 1 — Verificar Docker Desktop está corriendo

Docker Desktop debe estar abierto. Verificar:

```cmd
docker ps
```

Si no da error, Docker está listo.

---

### Paso 2 — Construir la imagen

```cmd
cd c:\Users\Hp\Desktop\devopsVV

docker build -t taskmanager:local .
```

Esto ejecuta el Dockerfile multi-stage (builder → runtime). Tarda 1-2 minutos la primera vez.

---

### Paso 3 — Levantar según el ambiente deseado

**Ambiente DEVELOPMENT** (con hot-reload, puerto 5000):

```cmd
docker compose --profile dev up
```

**Ambiente DEVELOPMENT** (reconstruir imagen y levantar):

```cmd
docker compose --profile dev up --build
```

**Ambiente TEST** (aislado, puerto 5001):

```cmd
docker compose --profile test up
```

**Ambiente PRODUCTION** (con Nginx como reverse proxy, puerto 80):

```cmd
docker compose --profile prod up
```

---

### Paso 4 — Verificar que los contenedores están corriendo

```cmd
docker ps
```

**Salida esperada para dev:**

```
CONTAINER ID   IMAGE              STATUS          PORTS
abc123...      taskmanager:dev    Up (healthy)    0.0.0.0:5000->5000/tcp
```

---

### Paso 5 — Probar la aplicación en Docker

```cmd
:: Health check
curl http://localhost:5000/api/health

:: Crear una tarea de prueba
curl -X POST http://localhost:5000/api/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Tarea Docker\", \"description\": \"Probando en contenedor\", \"status\": \"pending\"}"

:: Listar tareas
curl http://localhost:5000/api/tasks
```

Para PRODUCCIÓN (puerto 80):

```cmd
curl http://localhost:80/api/health
```

---

### Paso 6 — Detener los contenedores

```cmd
:: Detener (mantiene los volúmenes)
docker compose --profile dev down

:: Detener y eliminar volúmenes (base de datos)
docker compose --profile dev down -v
```

---

### Paso 7 — Ver logs del contenedor

```cmd
docker logs taskmanager_dev

:: Ver logs en tiempo real
docker logs -f taskmanager_dev
```

---

## 4. Instalación y Ejecución en GitHub Codespaces

### Paso 1 — Acceder al repositorio en GitHub

Ir a: **https://github.com/IvanPulgar/devopsVV**

---

### Paso 2 — Abrir Codespace

1. Clic en el botón verde **Code**
2. Seleccionar la pestaña **Codespaces**
3. Clic en **Create codespace on main**

Se abrirá un entorno VS Code en el navegador con Linux Ubuntu. Esto tarda 1-2 minutos.

---

### Paso 3 — En la terminal del Codespace (Linux)

```bash
# Verificar que estás en la carpeta correcta
pwd
# Debe mostrar: /workspaces/devopsVV

# Instalar dependencias
pip install -r requirements.txt
```

---

### Paso 4 — Configurar variables y levantar la app

```bash
export DATABASE_PATH=/tmp/taskmanager.db
export APP_ENV=development
export DEBUG=true
export PORT=5000
export HOST=0.0.0.0

python run.py
```

**Salida esperada:**

```
  Task Manager corriendo en http://0.0.0.0:5000
  Ambiente: development
 * Running on http://127.0.0.1:5000
 * Running on http://10.0.10.x:5000
```

---

### Paso 5 — Acceder a la URL pública del Codespace

Codespaces genera automáticamente una URL pública cuando un puerto es expuesto.

1. En VS Code (web), abrir el panel **PORTS** (pestaña en la barra inferior)
2. Buscar el puerto **5000**
3. Clic en el ícono de globo o copiar la URL que tiene el formato:
   `https://IvanPulgar-devopsvv-xxxx-5000.app.github.dev`

Esa URL es accesible públicamente desde cualquier navegador.

---

### Paso 6 — Verificar en el Codespace

```bash
# Health check
curl http://localhost:5000/api/health

# Crear una tarea de prueba
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Tarea en la nube", "description": "Probando en Codespaces", "status": "pending"}'

# Listar tareas
curl http://localhost:5000/api/tasks
```

---

## 5. Ejecución de las 245 Pruebas

### 5.1 Preparación

**En LOCAL (Windows) — antes de correr cualquier prueba:**

```cmd
cd c:\Users\Hp\Desktop\devopsVV
.venv\Scripts\activate
```

**En CODESPACES (Linux) — antes de correr cualquier prueba:**

```bash
cd /workspaces/devopsVV
pip install -r requirements.txt
```

> **Importante:** Las pruebas NO requieren que la aplicación esté corriendo. Cada test crea su propia instancia de Flask con una base de datos temporal. Pueden ejecutarse en cualquier momento sin levantar el servidor.

---

### 5.2 Comando para ejecutar TODAS las pruebas de una vez

**Windows (CMD o PowerShell):**

```cmd
py -m pytest -v
```

**Linux / Codespaces:**

```bash
python -m pytest -v
```

**Resultado esperado:**

```
============================= test session starts =============================
platform win32 -- Python 3.13.x, pytest-8.2.2
collected 245 items

tests/test_ci.py::...          46 passed
tests/test_infra.py::...       50 passed
tests/test_scripts.py::...     64 passed
tests/test_tasks.py::...       27 passed
tests/test_vv.py::...          58 passed

========================== 245 passed in ~12s =================================
```

---

### 5.3 GRUPO 1 — Pruebas API REST (27 tests) — test_tasks.py

Estas pruebas verifican todos los endpoints CRUD de la API.

**Ejecutar el grupo completo:**

```cmd
py -m pytest tests/test_tasks.py -v
```

**Ejecutar por subgrupos:**

```cmd
:: Health check (T-001, T-002)
py -m pytest tests/test_tasks.py::TestHealth -v

:: Listado de tareas (T-003 a T-006)
py -m pytest tests/test_tasks.py::TestListTasks -v

:: Creación de tareas (T-007 a T-015)
py -m pytest tests/test_tasks.py::TestCreateTask -v

:: Obtener tarea individual (T-016, T-017)
py -m pytest tests/test_tasks.py::TestGetTask -v

:: Actualizar tarea (T-018 a T-023)
py -m pytest tests/test_tasks.py::TestUpdateTask -v

:: Eliminar tarea (T-024 a T-027)
py -m pytest tests/test_tasks.py::TestDeleteTask -v
```

**Ejecutar una prueba específica por nombre:**

```cmd
py -m pytest tests/test_tasks.py::TestHealth::test_health_returns_200 -v
py -m pytest tests/test_tasks.py::TestCreateTask::test_create_returns_201 -v
py -m pytest tests/test_tasks.py::TestDeleteTask::test_delete_nonexistent_returns_404 -v
```

---

### 5.4 GRUPO 2 — Pruebas de Infraestructura Docker (50 tests) — test_infra.py

Estas pruebas validan la configuración de Docker, docker-compose, Nginx y archivos .env. **No requieren Docker corriendo**, solo los archivos de configuración.

**Ejecutar el grupo completo:**

```cmd
py -m pytest tests/test_infra.py -v
```

**Ejecutar por subgrupos:**

```cmd
:: Variables de entorno .env (I-001 a I-013)
py -m pytest tests/test_infra.py::TestEnvFiles -v

:: Dockerfile multi-stage (I-014 a I-021)
py -m pytest tests/test_infra.py::TestDockerfile -v

:: Docker Compose (I-022 a I-035)
py -m pytest tests/test_infra.py::TestDockerCompose -v

:: Configuración Nginx (I-036 a I-045)
py -m pytest tests/test_infra.py::TestNginxConfig -v

:: .dockerignore (I-046 a I-050)
py -m pytest tests/test_infra.py::TestDockerIgnore -v
```

---

### 5.5 GRUPO 3 — Pruebas de Scripts de Automatización (64 tests) — test_scripts.py

Estas pruebas validan la existencia, estructura y ejecución de los 10 scripts.

**Ejecutar el grupo completo:**

```cmd
py -m pytest tests/test_scripts.py -v
```

**Ejecutar por subgrupos:**

```cmd
:: Existencia de scripts (S-001 a S-012)
py -m pytest tests/test_scripts.py::TestScriptExistence -v

:: Estructura scripts Bash (S-013 a S-034)
py -m pytest tests/test_scripts.py::TestBashScriptStructure -v

:: Estructura scripts PowerShell (S-035 a S-051)
py -m pytest tests/test_scripts.py::TestPowerShellScriptStructure -v

:: Archivos de configuración (S-052 a S-060)
py -m pytest tests/test_scripts.py::TestConfigFiles -v

:: Ejecución real de scripts (S-061 a S-064)
py -m pytest tests/test_scripts.py::TestScriptExecution -v
```

---

### 5.6 GRUPO 4 — Pruebas de Pipeline CI/CD (46 tests) — test_ci.py

Estas pruebas validan los archivos GitHub Actions `.yml`.

**Ejecutar el grupo completo:**

```cmd
py -m pytest tests/test_ci.py -v
```

**Ejecutar por subgrupos:**

```cmd
:: Existencia de workflows (C-001 a C-003)
py -m pytest tests/test_ci.py::TestWorkflowExistence -v

:: Validez YAML (C-004, C-005)
py -m pytest tests/test_ci.py::TestYamlValidity -v

:: Estructura del pipeline CI (C-006 a C-031)
py -m pytest tests/test_ci.py::TestCIPipelineStructure -v

:: Workflow de publicación Docker (C-032 a C-040)
py -m pytest tests/test_ci.py::TestDockerPublishWorkflow -v

:: Consistencia del proyecto (C-041 a C-046)
py -m pytest tests/test_ci.py::TestProjectConsistency -v
```

---

### 5.7 GRUPO 5 — Pruebas V&V Ampliadas (58 tests) — test_vv.py

Este es el módulo principal de Verificación y Validación con 5 categorías.

**Ejecutar el grupo completo:**

```cmd
py -m pytest tests/test_vv.py -v
```

**VV-F — Funcionales (15 tests):**

```cmd
py -m pytest tests/test_vv.py::TestVV_Funcionales -v
```

Pruebas individuales:

```cmd
:: VV-F-01: Crear tarea con todos los campos
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_crear_tarea_con_todos_los_campos -v

:: VV-F-02: Timestamps al crear
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_tarea_tiene_timestamps_al_crear -v

:: VV-F-03: updated_at cambia al actualizar
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_updated_at_cambia_en_actualizacion -v

:: VV-F-04: created_at NO cambia al actualizar
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_created_at_no_cambia_en_actualizacion -v

:: VV-F-05: Ordenamiento más reciente primero
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_listar_tareas_ordena_mas_recientes_primero -v

:: VV-F-06: Filtro por in_progress
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_filtrar_por_status_in_progress -v

:: VV-F-07: Filtro por completed
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_filtrar_por_status_completed -v

:: VV-F-08: Filtro no contamina entre estados
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_filtro_no_contamina_entre_estados -v

:: VV-F-09: Actualizar solo descripción
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_actualizar_descripcion -v

:: VV-F-10: Actualizar múltiples campos
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_actualizar_multiples_campos_simultaneamente -v

:: VV-F-11: DELETE retorna confirmación
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_respuesta_delete_contiene_mensaje -v

:: VV-F-12: Tarea creada aparece en listado
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_tarea_creada_aparece_en_listado -v

:: VV-F-13: Tarea eliminada no aparece en listado
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_tarea_eliminada_no_aparece_en_listado -v

:: VV-F-14: Health devuelve service name
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_health_devuelve_service_name_correcto -v

:: VV-F-15: IDs únicos y autoincrement
py -m pytest tests/test_vv.py::TestVV_Funcionales::test_ids_son_unicos_y_autoincrementados -v
```

**VV-N — Negativos (12 tests):**

```cmd
py -m pytest tests/test_vv.py::TestVV_Negativos -v
```

Pruebas individuales:

```cmd
:: VV-N-01: Sin Content-Type JSON → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_crear_sin_content_type_json -v

:: VV-N-02: Título solo espacios → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_crear_con_title_solo_espacios -v

:: VV-N-03: status=null no genera 500
py -m pytest tests/test_vv.py::TestVV_Negativos::test_crear_con_status_null -v

:: VV-N-04: JSON malformado → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_crear_con_json_malformado -v

:: VV-N-05: PUT sin body → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_actualizar_sin_body -v

:: VV-N-06: PUT status inválido → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_actualizar_status_invalido -v

:: VV-N-07: PUT title=null → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_actualizar_title_null -v

:: VV-N-08: GET id=0 → 404
py -m pytest tests/test_vv.py::TestVV_Negativos::test_get_id_cero -v

:: VV-N-09: DELETE id inexistente → 404
py -m pytest tests/test_vv.py::TestVV_Negativos::test_delete_id_inexistente -v

:: VV-N-10: Error tiene campo 'error'
py -m pytest tests/test_vv.py::TestVV_Negativos::test_respuesta_error_tiene_campo_error -v

:: VV-N-11: Filtro inválido → 400
py -m pytest tests/test_vv.py::TestVV_Negativos::test_filtro_invalido_retorna_400 -v

:: VV-N-12: Ruta inexistente → 404
py -m pytest tests/test_vv.py::TestVV_Negativos::test_ruta_inexistente -v
```

**VV-B — Borde (14 tests):**

```cmd
py -m pytest tests/test_vv.py::TestVV_Borde -v
```

Pruebas individuales:

```cmd
:: VV-B-01: Título de 1 carácter
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_un_caracter -v

:: VV-B-02: Título de 1000 caracteres
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_mil_caracteres -v

:: VV-B-03: Descripción vacía aceptada
py -m pytest tests/test_vv.py::TestVV_Borde::test_descripcion_vacia_aceptada -v

:: VV-B-04: Descripción de 2000 caracteres
py -m pytest tests/test_vv.py::TestVV_Borde::test_descripcion_dos_mil_caracteres -v

:: VV-B-05: Título con emojis
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_con_emojis -v

:: VV-B-06: Título con caracteres chinos
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_con_caracteres_chinos -v

:: VV-B-07: HTML almacenado como texto plano
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_con_html -v

:: VV-B-08: SQL injection no vulnerable
py -m pytest tests/test_vv.py::TestVV_Borde::test_sql_injection_en_titulo -v

:: VV-B-09: Crear 100 tareas
py -m pytest tests/test_vv.py::TestVV_Borde::test_crear_cien_tareas -v

:: VV-B-10: ID=0 → 404
py -m pytest tests/test_vv.py::TestVV_Borde::test_id_cero_retorna_404 -v

:: VV-B-11: ID negativo → 404 o 405
py -m pytest tests/test_vv.py::TestVV_Borde::test_id_negativo -v

:: VV-B-12: Título solo tabulaciones → 400
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_solo_tabs -v

:: VV-B-13: Título solo saltos de línea → 400
py -m pytest tests/test_vv.py::TestVV_Borde::test_titulo_solo_newlines -v

:: VV-B-14: Body JSON vacío {} → 400
py -m pytest tests/test_vv.py::TestVV_Borde::test_body_json_vacio -v
```

**VV-I — Integración (7 tests):**

```cmd
py -m pytest tests/test_vv.py::TestVV_Integracion -v
```

Pruebas individuales:

```cmd
:: VV-I-01: Flujo CRUD completo
py -m pytest tests/test_vv.py::TestVV_Integracion::test_flujo_crud_completo -v

:: VV-I-02: Transición de estados
py -m pytest tests/test_vv.py::TestVV_Integracion::test_transicion_de_estados -v

:: VV-I-03: Modificar A no afecta B
py -m pytest tests/test_vv.py::TestVV_Integracion::test_modificar_tarea_a_no_afecta_b -v

:: VV-I-04: Eliminar B no elimina A
py -m pytest tests/test_vv.py::TestVV_Integracion::test_eliminar_b_no_elimina_a -v

:: VV-I-05: Cambio de estado se refleja en filtros
py -m pytest tests/test_vv.py::TestVV_Integracion::test_cambio_estado_se_refleja_en_filtros -v

:: VV-I-06: Actualizar un campo preserva los demás
py -m pytest tests/test_vv.py::TestVV_Integracion::test_actualizar_campo_preserva_resto -v

:: VV-I-07: Listado vacío al eliminar todo
py -m pytest tests/test_vv.py::TestVV_Integracion::test_listado_vacio_tras_eliminar_todo -v
```

**VV-H — HTTP (10 tests):**

```cmd
py -m pytest tests/test_vv.py::TestVV_HTTP -v
```

Pruebas individuales:

```cmd
:: VV-H-01: Content-Type JSON en todas las respuestas
py -m pytest tests/test_vv.py::TestVV_HTTP::test_todas_respuestas_son_json -v

:: VV-H-02: POST retorna 201
py -m pytest tests/test_vv.py::TestVV_HTTP::test_post_retorna_201 -v

:: VV-H-03: GET retorna 200
py -m pytest tests/test_vv.py::TestVV_HTTP::test_get_retorna_200 -v

:: VV-H-04: PUT retorna 200
py -m pytest tests/test_vv.py::TestVV_HTTP::test_put_retorna_200 -v

:: VV-H-05: DELETE retorna 200
py -m pytest tests/test_vv.py::TestVV_HTTP::test_delete_retorna_200 -v

:: VV-H-06: Errores 400 tienen body JSON
py -m pytest tests/test_vv.py::TestVV_HTTP::test_errores_400_incluyen_body_json -v

:: VV-H-07: Errores 404 tienen body JSON
py -m pytest tests/test_vv.py::TestVV_HTTP::test_errores_404_incluyen_body_json -v

:: VV-H-08: Listado es array JSON
py -m pytest tests/test_vv.py::TestVV_HTTP::test_listado_es_array_json -v

:: VV-H-09: Tarea individual es objeto JSON
py -m pytest tests/test_vv.py::TestVV_HTTP::test_tarea_individual_es_objeto_json -v

:: VV-H-10: Campos obligatorios en respuesta
py -m pytest tests/test_vv.py::TestVV_HTTP::test_campos_obligatorios_en_respuesta -v
```

---

### 5.8 Comandos adicionales útiles para las pruebas

**Ejecutar con salida detallada y sin truncar:**

```cmd
py -m pytest -v --tb=long
```

**Ejecutar con resumen al final (recomendado para documentar):**

```cmd
py -m pytest -v --tb=short 2>&1
```

**Ejecutar solo las pruebas que fallaron la última vez:**

```cmd
py -m pytest --lf -v
```

**Ejecutar por palabra clave (ej. todas las negativas):**

```cmd
py -m pytest -k "negativo or Negativo" -v
py -m pytest -k "borde or Borde" -v
py -m pytest -k "integracion or Integracion" -v
```

**Ejecutar y generar reporte XML (para evidencia):**

```cmd
py -m pytest --junitxml=resultados_pruebas.xml -v
```

**Ejecutar y guardar la salida en un archivo de texto:**

```cmd
py -m pytest -v > resultados_pruebas.txt 2>&1
type resultados_pruebas.txt
```

**Contar cuántos tests hay sin ejecutarlos:**

```cmd
py -m pytest --collect-only -q
```

---

### 5.9 Ejecutar análisis estático (lint)

```cmd
:: Verificar calidad del código (debe salir sin errores)
py -m flake8 app/
echo Exit code: %errorlevel%
```

Salida esperada: ningún mensaje (código 0 = sin errores).

---

### 5.10 Ejecutar en CODESPACES (mismos tests, comando diferente)

En la terminal del Codespace usar `python` en lugar de `py`:

```bash
# Todos los tests
python -m pytest -v

# Por grupo
python -m pytest tests/test_tasks.py -v
python -m pytest tests/test_infra.py -v
python -m pytest tests/test_scripts.py -v
python -m pytest tests/test_ci.py -v
python -m pytest tests/test_vv.py -v

# Solo VV ampliado por categoría
python -m pytest tests/test_vv.py::TestVV_Funcionales -v
python -m pytest tests/test_vv.py::TestVV_Negativos -v
python -m pytest tests/test_vv.py::TestVV_Borde -v
python -m pytest tests/test_vv.py::TestVV_Integracion -v
python -m pytest tests/test_vv.py::TestVV_HTTP -v

# Guardar resultado
python -m pytest -v > resultados_codespaces.txt 2>&1
cat resultados_codespaces.txt
```

---

## 6. Cómo Evidenciar y Documentar la Ejecución

### 6.1 Evidencia mínima recomendada

Para documentar correctamente la ejecución de las pruebas, recolecta las siguientes evidencias:

| Evidencia | Cómo obtenerla |
|---|---|
| Screenshot de los 245 tests pasando | Ejecutar `py -m pytest -v` y tomar captura de pantalla |
| Archivo de resultados en texto | `py -m pytest -v > resultados.txt 2>&1` |
| Reporte XML (formato JUnit) | `py -m pytest --junitxml=resultados.xml -v` |
| Screenshot de la app corriendo | Navegador en http://localhost:5000 |
| Screenshot del health check | `curl http://localhost:5000/api/health` |
| URL pública (Codespaces) | URL del panel Ports en VS Code web |

---

### 6.2 Flujo de demostración recomendado

**Paso 1 — Mostrar la estructura del proyecto:**

```cmd
dir c:\Users\Hp\Desktop\devopsVV /s /b | findstr /V ".pyc" | findstr /V "__pycache__" | findstr /V ".git"
```

**Paso 2 — Mostrar los 3 ambientes:**

```cmd
type .env.dev
type .env.test
type .env.prod
```

**Paso 3 — Levantar la aplicación:**

```cmd
.venv\Scripts\activate
set DATABASE_PATH=taskmanager.db
py run.py
```

**Paso 4 — Probar la API manualmente:**

```cmd
curl http://localhost:5000/api/health
curl http://localhost:5000/api/tasks
curl -X POST http://localhost:5000/api/tasks -H "Content-Type: application/json" -d "{\"title\":\"Evidencia\",\"status\":\"pending\"}"
```

**Paso 5 — Ejecutar todos los tests (en otra terminal):**

```cmd
cd c:\Users\Hp\Desktop\devopsVV
.venv\Scripts\activate
py -m pytest -v 2>&1 | tee resultados_finales.txt
```

**Paso 6 — Ejecutar lint:**

```cmd
py -m flake8 app/
echo Lint OK - exit code: %errorlevel%
```

**Paso 7 — Mostrar los documentos:**

```cmd
:: Abrir el plan V&V
start docs\plan_vv.docx

:: Abrir el documento técnico
start docs\documento_tecnico.docx
```

---

### 6.3 Errores conocidos y sus soluciones

| Error | Causa | Solución |
|---|---|---|
| `'py' no se reconoce` | Python Launcher no está en PATH | Usar la ruta completa: `C:\Users\...\py.exe` |
| `ModuleNotFoundError: flask` | Entorno virtual no activado | Ejecutar `.venv\Scripts\activate` |
| `DATABASE_PATH not set` | Variable de entorno no configurada | `set DATABASE_PATH=taskmanager.db` |
| `Address already in use` | Puerto 5000 ocupado | Cambiar con `set PORT=5001` |
| `docker: command not found` | Docker Desktop no instalado/corriendo | Abrir Docker Desktop |
| `Repository not found` | Repo no existe en GitHub | Crear el repo en github.com/new |

---

### 6.4 Interpretación de los resultados

Cuando ejecutas `py -m pytest -v`, cada línea muestra:

```
tests/test_tasks.py::TestHealth::test_health_returns_200 PASSED    [  0%]
tests/test_tasks.py::TestHealth::test_health_body_ok PASSED        [  0%]
```

- **PASSED** = prueba exitosa ✅
- **FAILED** = prueba fallida ❌ (se muestra el detalle del error)
- **ERROR** = error en el setup del test (no en la lógica)
- **SKIPPED** = prueba omitida

Al final aparece el resumen:

```
========================== 245 passed in 13.06s ===========================
```

**245 passed = proyecto completamente funcional y validado.**
