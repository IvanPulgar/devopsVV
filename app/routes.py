from flask import Blueprint, jsonify, request
from .database import get_db

tasks_bp = Blueprint('tasks', __name__)

VALID_STATUSES = ('pending', 'in_progress', 'completed')


# ── Health ────────────────────────────────────────────────────────────────────

@tasks_bp.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'task-manager'})


# ── List ──────────────────────────────────────────────────────────────────────

@tasks_bp.route('/api/tasks', methods=['GET'])
def list_tasks():
    status = request.args.get('status')
    db = get_db()
    try:
        if status:
            if status not in VALID_STATUSES:
                return jsonify({'error': f'Estado inválido. Válidos: {list(VALID_STATUSES)}'}), 400
            rows = db.execute(
                'SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC, id DESC',
                (status,)
            ).fetchall()
        else:
            rows = db.execute(
                'SELECT * FROM tasks ORDER BY created_at DESC, id DESC'
            ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        db.close()


# ── Get one ───────────────────────────────────────────────────────────────────

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    db = get_db()
    try:
        row = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if row is None:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        return jsonify(dict(row))
    finally:
        db.close()


# ── Create ────────────────────────────────────────────────────────────────────

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Se requiere cuerpo JSON'}), 400

    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'El título es requerido'}), 400

    description = (data.get('description') or '').strip()
    status = data.get('status', 'pending')
    if status not in VALID_STATUSES:
        return jsonify({'error': f'Estado inválido. Válidos: {list(VALID_STATUSES)}'}), 400

    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
            (title, description, status)
        )
        db.commit()
        row = db.execute('SELECT * FROM tasks WHERE id = ?', (cursor.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    finally:
        db.close()


# ── Update ────────────────────────────────────────────────────────────────────

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Se requiere cuerpo JSON'}), 400

    db = get_db()
    try:
        row = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if row is None:
            return jsonify({'error': 'Tarea no encontrada'}), 404

        if 'title' in data:
            title = (data['title'] or '').strip()
            if not title:
                return jsonify({'error': 'El título no puede estar vacío'}), 400
        else:
            title = row['title']

        description = data.get('description', row['description'])
        status = data.get('status', row['status'])
        if status not in VALID_STATUSES:
            return jsonify({'error': f'Estado inválido. Válidos: {list(VALID_STATUSES)}'}), 400

        db.execute(
            """UPDATE tasks
               SET title = ?, description = ?, status = ?,
                   updated_at = datetime('now')
               WHERE id = ?""",
            (title, description, status, task_id)
        )
        db.commit()
        updated = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return jsonify(dict(updated))
    finally:
        db.close()


# ── Delete ────────────────────────────────────────────────────────────────────

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    try:
        row = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if row is None:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        return jsonify({'message': 'Tarea eliminada exitosamente', 'id': task_id})
    finally:
        db.close()
