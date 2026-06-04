"""
Fase 1 – Suite de pruebas básicas del Task Manager
Cubre: Health, CRUD funcional, casos negativos y borde.
Suite completa de V&V (Fase 5) amplía estos casos.
"""
import json
import pytest


# ── Helper ────────────────────────────────────────────────────────────────────

def post_task(client, title='Tarea de prueba', description='', status='pending'):
    return client.post(
        '/api/tasks',
        data=json.dumps({'title': title, 'description': description, 'status': status}),
        content_type='application/json'
    )


def get_json(response):
    return json.loads(response.data)


# ── Health check ──────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_200(self, client):
        assert client.get('/api/health').status_code == 200

    def test_health_body_ok(self, client):
        data = get_json(client.get('/api/health'))
        assert data['status']  == 'ok'
        assert data['service'] == 'task-manager'


# ── GET /api/tasks ────────────────────────────────────────────────────────────

class TestListTasks:
    def test_empty_list_on_clean_db(self, client):
        res = client.get('/api/tasks')
        assert res.status_code == 200
        assert get_json(res) == []

    def test_returns_created_tasks(self, client):
        post_task(client, 'Tarea A')
        post_task(client, 'Tarea B')
        tasks = get_json(client.get('/api/tasks'))
        assert len(tasks) == 2

    def test_filter_by_status_pending(self, client):
        post_task(client, 'P1', status='pending')
        post_task(client, 'P2', status='completed')
        tasks = get_json(client.get('/api/tasks?status=pending'))
        assert all(t['status'] == 'pending' for t in tasks)
        assert len(tasks) == 1

    def test_filter_by_invalid_status_returns_400(self, client):
        assert client.get('/api/tasks?status=invalido').status_code == 400


# ── POST /api/tasks ───────────────────────────────────────────────────────────

class TestCreateTask:
    def test_create_returns_201(self, client):
        assert post_task(client).status_code == 201

    def test_create_response_has_required_fields(self, client):
        data = get_json(post_task(client, 'Campos', 'Descripción', 'in_progress'))
        assert data['id']          is not None
        assert data['title']       == 'Campos'
        assert data['description'] == 'Descripción'
        assert data['status']      == 'in_progress'
        assert 'created_at'        in data
        assert 'updated_at'        in data

    def test_default_status_is_pending(self, client):
        res = client.post('/api/tasks',
                          data=json.dumps({'title': 'Sin estado'}),
                          content_type='application/json')
        assert get_json(res)['status'] == 'pending'

    # Casos negativos
    def test_create_without_title_returns_400(self, client):
        res = client.post('/api/tasks',
                          data=json.dumps({'description': 'sin título'}),
                          content_type='application/json')
        assert res.status_code == 400

    def test_create_with_empty_title_returns_400(self, client):
        res = client.post('/api/tasks',
                          data=json.dumps({'title': '   '}),
                          content_type='application/json')
        assert res.status_code == 400

    def test_create_with_invalid_status_returns_400(self, client):
        assert post_task(client, status='estado_invalido').status_code == 400

    def test_create_without_json_body_returns_400(self, client):
        assert client.post('/api/tasks').status_code == 400

    # Casos borde
    def test_create_with_very_long_title(self, client):
        long_title = 'A' * 500
        res = post_task(client, title=long_title)
        assert res.status_code == 201
        assert get_json(res)['title'] == long_title

    def test_create_with_special_characters(self, client):
        title = '<script>alert("xss")</script> & "comillas" \'simples\''
        res   = post_task(client, title=title)
        assert res.status_code == 201
        assert get_json(res)['title'] == title   # almacenado tal cual; el escape es del frontend


# ── GET /api/tasks/<id> ───────────────────────────────────────────────────────

class TestGetTask:
    def test_get_existing_task(self, client):
        task_id = get_json(post_task(client, 'Obtener'))['id']
        res     = client.get(f'/api/tasks/{task_id}')
        assert res.status_code == 200
        assert get_json(res)['id'] == task_id

    def test_get_nonexistent_returns_404(self, client):
        assert client.get('/api/tasks/99999').status_code == 404


# ── PUT /api/tasks/<id> ───────────────────────────────────────────────────────

class TestUpdateTask:
    def test_update_status_to_completed(self, client):
        task_id = get_json(post_task(client, 'Completar'))['id']
        res     = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({'status': 'completed'}),
                             content_type='application/json')
        assert res.status_code == 200
        assert get_json(res)['status'] == 'completed'

    def test_update_title(self, client):
        task_id = get_json(post_task(client, 'Título viejo'))['id']
        res     = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({'title': 'Título nuevo'}),
                             content_type='application/json')
        assert get_json(res)['title'] == 'Título nuevo'

    def test_update_preserves_unmodified_fields(self, client):
        task_id = get_json(post_task(client, 'Preservar', 'Descripción original'))['id']
        client.put(f'/api/tasks/{task_id}',
                   data=json.dumps({'status': 'in_progress'}),
                   content_type='application/json')
        updated = get_json(client.get(f'/api/tasks/{task_id}'))
        assert updated['description'] == 'Descripción original'

    # Casos negativos
    def test_update_nonexistent_returns_404(self, client):
        res = client.put('/api/tasks/99999',
                         data=json.dumps({'title': 'x'}),
                         content_type='application/json')
        assert res.status_code == 404

    def test_update_with_empty_title_returns_400(self, client):
        task_id = get_json(post_task(client, 'Original'))['id']
        res     = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({'title': ''}),
                             content_type='application/json')
        assert res.status_code == 400

    def test_update_with_invalid_status_returns_400(self, client):
        task_id = get_json(post_task(client, 'Estado'))['id']
        res     = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({'status': 'desconocido'}),
                             content_type='application/json')
        assert res.status_code == 400


# ── DELETE /api/tasks/<id> ────────────────────────────────────────────────────

class TestDeleteTask:
    def test_delete_existing_task_returns_200(self, client):
        task_id = get_json(post_task(client, 'Borrar'))['id']
        assert client.delete(f'/api/tasks/{task_id}').status_code == 200

    def test_deleted_task_not_found_afterwards(self, client):
        task_id = get_json(post_task(client, 'Borrar y verificar'))['id']
        client.delete(f'/api/tasks/{task_id}')
        assert client.get(f'/api/tasks/{task_id}').status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        assert client.delete('/api/tasks/99999').status_code == 404

    # Caso borde: eliminar la misma tarea dos veces
    def test_double_delete_returns_404_second_time(self, client):
        task_id = get_json(post_task(client, 'Doble borrado'))['id']
        client.delete(f'/api/tasks/{task_id}')
        assert client.delete(f'/api/tasks/{task_id}').status_code == 404
