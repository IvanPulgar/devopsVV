"""
tests/test_vv.py
─────────────────────────────────────────────────────────────────────────────
Fase 5 – Suite completa de Verificación y Validación (V&V)

Organización por niveles de prueba:
  VV-F  Funcionales (flujos completos)
  VV-N  Negativos   (entradas inválidas, restricciones)
  VV-B  Borde       (límites, valores extremos)
  VV-I  Integración (encadenamiento de operaciones)
  VV-H  HTTP        (cabeceras, métodos, códigos de estado)
─────────────────────────────────────────────────────────────────────────────
"""
import json
import time

import pytest


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades compartidas
# ─────────────────────────────────────────────────────────────────────────────
def mk_task(client, title="Tarea VV", description="", status="pending"):
    res = client.post(
        "/api/tasks",
        data=json.dumps({"title": title, "description": description, "status": status}),
        content_type="application/json",
    )
    return res


def get_json(response):
    return json.loads(response.data)


def create_and_get_id(client, title="Tarea VV", **kw):
    return get_json(mk_task(client, title, **kw))["id"]


# ─────────────────────────────────────────────────────────────────────────────
# VV-F · Funcionales
# ─────────────────────────────────────────────────────────────────────────────
class TestVV_Funcionales:
    """VV-F: Verificación de comportamiento funcional correcto."""

    # VV-F-01
    def test_crear_tarea_con_todos_los_campos(self, client):
        """La API debe aceptar title, description y status simultáneamente."""
        res = mk_task(client, "Completa", "Descripción detallada", "in_progress")
        assert res.status_code == 201
        data = get_json(res)
        assert data["title"] == "Completa"
        assert data["description"] == "Descripción detallada"
        assert data["status"] == "in_progress"

    # VV-F-02
    def test_tarea_tiene_timestamps_al_crear(self, client):
        """Toda tarea recién creada debe tener created_at y updated_at."""
        data = get_json(mk_task(client, "Timestamps"))
        assert data["created_at"] is not None
        assert data["updated_at"] is not None

    # VV-F-03
    def test_updated_at_cambia_en_actualizacion(self, client):
        """updated_at debe cambiar al actualizar una tarea."""
        task_id = create_and_get_id(client, "Actualizar tiempo")
        original = get_json(client.get(f"/api/tasks/{task_id}"))["updated_at"]
        # Forzar diferencia de tiempo (SQLite tiene precisión de segundos)
        time.sleep(1)
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"status": "completed"}),
            content_type="application/json",
        )
        updated = get_json(client.get(f"/api/tasks/{task_id}"))["updated_at"]
        assert updated != original, "updated_at debe cambiar al actualizar"

    # VV-F-04
    def test_created_at_no_cambia_en_actualizacion(self, client):
        """created_at NO debe cambiar al actualizar una tarea."""
        task_id = create_and_get_id(client, "Crear tiempo fijo")
        original_created = get_json(client.get(f"/api/tasks/{task_id}"))["created_at"]
        time.sleep(1)
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"title": "Nuevo título"}),
            content_type="application/json",
        )
        assert get_json(client.get(f"/api/tasks/{task_id}"))["created_at"] == original_created

    # VV-F-05
    def test_listar_tareas_ordena_mas_recientes_primero(self, client):
        """GET /api/tasks debe devolver tareas ordenadas de más reciente a más antigua."""
        id1 = create_and_get_id(client, "Primera")
        time.sleep(1)  # garantizar distinto created_at (precisión SQLite: segundos)
        id2 = create_and_get_id(client, "Segunda")
        tasks = get_json(client.get("/api/tasks"))
        ids = [t["id"] for t in tasks]
        assert ids.index(id2) < ids.index(id1), "Las tareas más recientes deben aparecer primero"

    # VV-F-06
    def test_filtrar_por_status_in_progress(self, client):
        mk_task(client, "En progreso", status="in_progress")
        mk_task(client, "Pendiente", status="pending")
        tasks = get_json(client.get("/api/tasks?status=in_progress"))
        assert len(tasks) >= 1
        assert all(t["status"] == "in_progress" for t in tasks)

    # VV-F-07
    def test_filtrar_por_status_completed(self, client):
        mk_task(client, "Completada", status="completed")
        mk_task(client, "Pendiente 2", status="pending")
        tasks = get_json(client.get("/api/tasks?status=completed"))
        assert all(t["status"] == "completed" for t in tasks)

    # VV-F-08
    def test_filtro_no_contamina_entre_estados(self, client):
        """El filtro por un estado no debe devolver tareas de otro estado."""
        mk_task(client, "Solo pending A", status="pending")
        mk_task(client, "Completada X", status="completed")
        pending = get_json(client.get("/api/tasks?status=pending"))
        assert all(t["status"] == "pending" for t in pending)

    # VV-F-09
    def test_actualizar_descripcion(self, client):
        task_id = create_and_get_id(client, "Desc original", description="Vieja")
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"description": "Nueva descripción"}),
            content_type="application/json",
        )
        assert get_json(client.get(f"/api/tasks/{task_id}"))["description"] == "Nueva descripción"

    # VV-F-10
    def test_actualizar_multiples_campos_simultaneamente(self, client):
        task_id = create_and_get_id(client, "Multi update")
        res = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({
                "title": "Título actualizado",
                "description": "Desc actualizada",
                "status": "completed",
            }),
            content_type="application/json",
        )
        data = get_json(res)
        assert data["title"] == "Título actualizado"
        assert data["description"] == "Desc actualizada"
        assert data["status"] == "completed"

    # VV-F-11
    def test_respuesta_delete_contiene_mensaje(self, client):
        """DELETE exitoso debe devolver un mensaje de confirmación."""
        task_id = create_and_get_id(client, "Eliminar")
        data = get_json(client.delete(f"/api/tasks/{task_id}"))
        assert "message" in data or "id" in data, \
            "DELETE debe devolver confirmación (message o id)"

    # VV-F-12
    def test_tarea_creada_aparece_en_listado(self, client):
        title = "Aparezco en listado"
        mk_task(client, title)
        tasks = get_json(client.get("/api/tasks"))
        titles = [t["title"] for t in tasks]
        assert title in titles

    # VV-F-13
    def test_tarea_eliminada_no_aparece_en_listado(self, client):
        task_id = create_and_get_id(client, "Eliminada del listado")
        client.delete(f"/api/tasks/{task_id}")
        tasks = get_json(client.get("/api/tasks"))
        ids = [t["id"] for t in tasks]
        assert task_id not in ids

    # VV-F-14
    def test_health_devuelve_service_name(self, client):
        data = get_json(client.get("/api/health"))
        assert data.get("service") == "task-manager"

    # VV-F-15
    def test_id_es_autoincrementado(self, client):
        """Los IDs asignados deben ser únicos y crecientes."""
        id1 = create_and_get_id(client, "Primera tarea")
        id2 = create_and_get_id(client, "Segunda tarea")
        assert id2 > id1


# ─────────────────────────────────────────────────────────────────────────────
# VV-N · Negativos
# ─────────────────────────────────────────────────────────────────────────────
class TestVV_Negativos:
    """VV-N: Verificación del manejo correcto de entradas inválidas."""

    # VV-N-01
    def test_crear_sin_content_type_json_retorna_400(self, client):
        """Sin Content-Type: application/json debe retornar 400."""
        res = client.post("/api/tasks", data='{"title":"sin ct"}')
        assert res.status_code == 400

    # VV-N-02
    def test_crear_con_title_solo_espacios_retorna_400(self, client):
        res = mk_task(client, "     ")
        assert res.status_code == 400

    # VV-N-03
    def test_crear_con_status_none_usa_default(self, client):
        """status=null en JSON debe ser rechazado o tratado como pending."""
        res = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Status null", "status": None}),
            content_type="application/json",
        )
        # Puede ser 201 con pending o 400 — no debe ser 500
        assert res.status_code in (200, 201, 400)
        assert res.status_code != 500

    # VV-N-04
    def test_crear_con_json_malformado_retorna_400(self, client):
        res = client.post(
            "/api/tasks",
            data="{titulo: sin comillas}",
            content_type="application/json",
        )
        assert res.status_code == 400

    # VV-N-05
    def test_actualizar_sin_body_retorna_400(self, client):
        task_id = create_and_get_id(client, "Sin body")
        res = client.put(f"/api/tasks/{task_id}")
        assert res.status_code == 400

    # VV-N-06
    def test_actualizar_status_invalido_retorna_400(self, client):
        task_id = create_and_get_id(client, "Estado malo")
        res = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"status": "ACTIVO"}),
            content_type="application/json",
        )
        assert res.status_code == 400

    # VV-N-07
    def test_actualizar_title_null_retorna_400(self, client):
        """Enviar title: null explícitamente debe retornar 400."""
        task_id = create_and_get_id(client, "Title null")
        res = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"title": None}),
            content_type="application/json",
        )
        assert res.status_code == 400

    # VV-N-08
    def test_get_id_inexistente_retorna_404(self, client):
        assert client.get("/api/tasks/0").status_code == 404

    # VV-N-09
    def test_delete_id_inexistente_retorna_404(self, client):
        assert client.delete("/api/tasks/999999").status_code == 404

    # VV-N-10
    def test_respuesta_error_tiene_campo_error(self, client):
        """Los errores 400/404 deben devolver JSON con campo 'error'."""
        res = mk_task(client, "")
        assert "error" in get_json(res)

    # VV-N-11
    def test_filtro_status_invalido_retorna_400_con_mensaje(self, client):
        res = client.get("/api/tasks?status=HECHO")
        assert res.status_code == 400
        assert "error" in get_json(res)

    # VV-N-12
    def test_get_ruta_inexistente_retorna_404(self, client):
        assert client.get("/api/ruta/que/no/existe").status_code == 404


# ─────────────────────────────────────────────────────────────────────────────
# VV-B · Borde
# ─────────────────────────────────────────────────────────────────────────────
class TestVV_Borde:
    """VV-B: Verificación en valores límite y casos extremos."""

    # VV-B-01
    def test_titulo_de_un_solo_caracter(self, client):
        res = mk_task(client, "X")
        assert res.status_code == 201
        assert get_json(res)["title"] == "X"

    # VV-B-02
    def test_titulo_de_1000_caracteres(self, client):
        long = "T" * 1000
        res = mk_task(client, long)
        assert res.status_code == 201
        assert get_json(res)["title"] == long

    # VV-B-03
    def test_descripcion_vacia_es_aceptada(self, client):
        res = mk_task(client, "Sin desc", description="")
        assert res.status_code == 201

    # VV-B-04
    def test_descripcion_de_2000_caracteres(self, client):
        long_desc = "D" * 2000
        res = mk_task(client, "Desc larga", description=long_desc)
        assert res.status_code == 201
        assert get_json(res)["description"] == long_desc

    # VV-B-05
    def test_titulo_con_unicode_emojis(self, client):
        title = "Tarea con emojis 🚀✅🐍"
        res = mk_task(client, title)
        assert res.status_code == 201
        assert get_json(res)["title"] == title

    # VV-B-06
    def test_titulo_con_caracteres_chinos(self, client):
        title = "任务管理器测试"
        res = mk_task(client, title)
        assert res.status_code == 201
        assert get_json(res)["title"] == title

    # VV-B-07
    def test_titulo_con_html_se_almacena_sin_escapar(self, client):
        """La API debe almacenar HTML como texto plano (escape es responsabilidad del frontend)."""
        title = '<b>Negrita</b> & <i>cursiva</i>'
        res = mk_task(client, title)
        assert res.status_code == 201
        assert get_json(res)["title"] == title

    # VV-B-08
    def test_titulo_con_comillas_sql_injection(self, client):
        """Verificar que comillas simples no rompen la consulta SQL."""
        title = "O'Brien's task; DROP TABLE tasks;--"
        res = mk_task(client, title)
        assert res.status_code == 201
        assert get_json(res)["title"] == title
        # La tabla sigue intacta
        assert client.get("/api/tasks").status_code == 200

    # VV-B-09
    def test_crear_100_tareas_y_listar(self, client):
        """La API debe manejar correctamente la creación masiva."""
        for i in range(100):
            mk_task(client, f"Tarea masiva {i:03d}")
        tasks = get_json(client.get("/api/tasks"))
        assert len(tasks) >= 100

    # VV-B-10
    def test_id_cero_no_encontrado(self, client):
        assert client.get("/api/tasks/0").status_code == 404

    # VV-B-11
    def test_id_negativo_no_encontrado_o_404(self, client):
        res = client.get("/api/tasks/-1")
        assert res.status_code in (404, 405), \
            "ID negativo debe devolver 404 o 405"

    # VV-B-12
    def test_titulo_con_solo_tab_retorna_400(self, client):
        res = mk_task(client, "\t\t\t")
        assert res.status_code == 400

    # VV-B-13
    def test_titulo_con_solo_newlines_retorna_400(self, client):
        res = mk_task(client, "\n\n\n")
        assert res.status_code == 400

    # VV-B-14
    def test_body_json_vacio_retorna_400(self, client):
        res = client.post(
            "/api/tasks",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert res.status_code == 400


# ─────────────────────────────────────────────────────────────────────────────
# VV-I · Integración (flujos encadenados)
# ─────────────────────────────────────────────────────────────────────────────
class TestVV_Integracion:
    """VV-I: Verificación de flujos completos de extremo a extremo."""

    # VV-I-01
    def test_flujo_completo_crud(self, client):
        """Crear → Leer → Actualizar → Eliminar en secuencia."""
        # Crear
        res_create = mk_task(client, "CRUD completo", "Desc inicial", "pending")
        assert res_create.status_code == 201
        task = get_json(res_create)
        tid = task["id"]

        # Leer
        res_get = client.get(f"/api/tasks/{tid}")
        assert res_get.status_code == 200
        assert get_json(res_get)["title"] == "CRUD completo"

        # Actualizar
        res_put = client.put(
            f"/api/tasks/{tid}",
            data=json.dumps({"status": "in_progress", "title": "CRUD actualizado"}),
            content_type="application/json",
        )
        assert res_put.status_code == 200
        updated = get_json(res_put)
        assert updated["status"] == "in_progress"
        assert updated["title"] == "CRUD actualizado"

        # Eliminar
        res_del = client.delete(f"/api/tasks/{tid}")
        assert res_del.status_code == 200

        # Verificar eliminación
        assert client.get(f"/api/tasks/{tid}").status_code == 404

    # VV-I-02
    def test_transicion_de_estados_pendiente_a_completado(self, client):
        """pending → in_progress → completed debe ser posible."""
        tid = create_and_get_id(client, "Transición")

        client.put(f"/api/tasks/{tid}",
                   data=json.dumps({"status": "in_progress"}),
                   content_type="application/json")
        assert get_json(client.get(f"/api/tasks/{tid}"))["status"] == "in_progress"

        client.put(f"/api/tasks/{tid}",
                   data=json.dumps({"status": "completed"}),
                   content_type="application/json")
        assert get_json(client.get(f"/api/tasks/{tid}"))["status"] == "completed"

    # VV-I-03
    def test_multiples_tareas_independientes(self, client):
        """Modificar una tarea no debe afectar a otras."""
        id_a = create_and_get_id(client, "Tarea A")
        id_b = create_and_get_id(client, "Tarea B")

        client.put(f"/api/tasks/{id_a}",
                   data=json.dumps({"status": "completed"}),
                   content_type="application/json")

        tarea_b = get_json(client.get(f"/api/tasks/{id_b}"))
        assert tarea_b["status"] == "pending", "Tarea B no debe verse afectada"
        assert tarea_b["title"] == "Tarea B"

    # VV-I-04
    def test_eliminar_no_afecta_otras_tareas(self, client):
        """Eliminar una tarea no debe eliminar las demás."""
        id_a = create_and_get_id(client, "Permanente")
        id_b = create_and_get_id(client, "Efímera")

        client.delete(f"/api/tasks/{id_b}")

        assert client.get(f"/api/tasks/{id_a}").status_code == 200

    # VV-I-05
    def test_filtro_refleja_actualizacion_de_estado(self, client):
        """Cambiar el estado de una tarea debe reflejarse en el filtro."""
        tid = create_and_get_id(client, "Cambio de filtro", status="pending")
        pending_before = get_json(client.get("/api/tasks?status=pending"))
        pending_ids_before = [t["id"] for t in pending_before]
        assert tid in pending_ids_before

        client.put(f"/api/tasks/{tid}",
                   data=json.dumps({"status": "completed"}),
                   content_type="application/json")

        pending_after = get_json(client.get("/api/tasks?status=pending"))
        pending_ids_after = [t["id"] for t in pending_after]
        assert tid not in pending_ids_after

        completed = get_json(client.get("/api/tasks?status=completed"))
        assert any(t["id"] == tid for t in completed)

    # VV-I-06
    def test_crear_actualizar_y_verificar_campos_individualmente(self, client):
        """Actualizar sólo un campo no debe borrar los demás."""
        tid = create_and_get_id(client, "Campos separados",
                                description="Descripción importante", status="pending")
        client.put(f"/api/tasks/{tid}",
                   data=json.dumps({"status": "completed"}),
                   content_type="application/json")
        task = get_json(client.get(f"/api/tasks/{tid}"))
        assert task["title"] == "Campos separados"
        assert task["description"] == "Descripción importante"
        assert task["status"] == "completed"

    # VV-I-07
    def test_listado_vacio_tras_eliminar_todas(self, client):
        """Después de eliminar todas las tareas, el listado debe estar vacío."""
        ids = [create_and_get_id(client, f"Del {i}") for i in range(3)]
        for tid in ids:
            client.delete(f"/api/tasks/{tid}")
        tasks = get_json(client.get("/api/tasks"))
        # No debe quedar ninguna de las que creamos
        remaining_ids = [t["id"] for t in tasks]
        for tid in ids:
            assert tid not in remaining_ids


# ─────────────────────────────────────────────────────────────────────────────
# VV-H · HTTP (cabeceras, métodos, respuestas)
# ─────────────────────────────────────────────────────────────────────────────
class TestVV_HTTP:
    """VV-H: Verificación de conformidad con el protocolo HTTP."""

    # VV-H-01
    def test_respuestas_son_json(self, client):
        """Todas las respuestas de la API deben tener Content-Type application/json."""
        endpoints = [
            ("GET",    "/api/health",  None),
            ("GET",    "/api/tasks",   None),
            ("POST",   "/api/tasks",   json.dumps({"title": "CT test"})),
        ]
        for method, url, data in endpoints:
            if method == "GET":
                res = client.get(url)
            else:
                res = client.post(url, data=data, content_type="application/json")
            assert "application/json" in res.content_type, \
                f"{method} {url} debe responder con Content-Type application/json"

    # VV-H-02
    def test_post_retorna_201_al_crear(self, client):
        res = mk_task(client, "POST 201")
        assert res.status_code == 201

    # VV-H-03
    def test_get_retorna_200(self, client):
        assert client.get("/api/tasks").status_code == 200

    # VV-H-04
    def test_put_retorna_200_en_actualizacion_exitosa(self, client):
        tid = create_and_get_id(client, "PUT 200")
        res = client.put(f"/api/tasks/{tid}",
                         data=json.dumps({"status": "completed"}),
                         content_type="application/json")
        assert res.status_code == 200

    # VV-H-05
    def test_delete_retorna_200_en_eliminacion_exitosa(self, client):
        tid = create_and_get_id(client, "DELETE 200")
        assert client.delete(f"/api/tasks/{tid}").status_code == 200

    # VV-H-06
    def test_errores_400_incluyen_body_json(self, client):
        """Respuestas de error 400 deben incluir cuerpo JSON."""
        res = mk_task(client, "")
        assert res.status_code == 400
        body = get_json(res)
        assert isinstance(body, dict), "El cuerpo del error debe ser un objeto JSON"

    # VV-H-07
    def test_errores_404_incluyen_body_json(self, client):
        """Respuestas 404 deben incluir cuerpo JSON."""
        res = client.get("/api/tasks/99999")
        assert res.status_code == 404
        body = get_json(res)
        assert isinstance(body, dict)

    # VV-H-08
    def test_respuesta_lista_es_array_json(self, client):
        """GET /api/tasks debe devolver un array JSON."""
        res = client.get("/api/tasks")
        data = get_json(res)
        assert isinstance(data, list), "La respuesta de /api/tasks debe ser un array"

    # VV-H-09
    def test_respuesta_tarea_individual_es_objeto_json(self, client):
        """GET /api/tasks/<id> debe devolver un objeto JSON."""
        tid = create_and_get_id(client, "Objeto JSON")
        data = get_json(client.get(f"/api/tasks/{tid}"))
        assert isinstance(data, dict)

    # VV-H-10
    def test_campos_obligatorios_en_respuesta_de_tarea(self, client):
        """Cada tarea en la respuesta debe tener id, title, description, status, created_at, updated_at."""
        tid = create_and_get_id(client, "Campos obligatorios")
        data = get_json(client.get(f"/api/tasks/{tid}"))
        for field in ("id", "title", "description", "status", "created_at", "updated_at"):
            assert field in data, f"El campo '{field}' debe estar presente en la respuesta"
