'use strict';

const API = '/api';
let currentFilter = '';
const cache = {};          // { id: taskObject }

// ── Utilidades ───────────────────────────────────────────────────────────────

function esc(str) {
    const d = document.createElement('div');
    d.textContent = String(str ?? '');
    return d.innerHTML;
}

function fmtDate(s) {
    if (!s) return '';
    // SQLite guarda sin 'Z', lo agregamos para que Date lo interprete como UTC
    return new Date(s.endsWith('Z') ? s : s + 'Z')
        .toLocaleString('es-ES', {
            day: '2-digit', month: 'short', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
}

const LABEL = { pending: 'Pendiente', in_progress: 'En Progreso', completed: 'Completada' };
const ICON  = { pending: '⏳',        in_progress: '🔄',          completed: '✅'         };

// ── API helper ────────────────────────────────────────────────────────────────

async function apiFetch(method, path, body) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body !== undefined) opts.body = JSON.stringify(body);
    const res  = await fetch(API + path, opts);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
}

// ── Render ────────────────────────────────────────────────────────────────────

function taskCard(task) {
    cache[task.id] = task;
    return `
    <article class="task-card" data-id="${task.id}" data-status="${task.status}">
        <div class="task-header">
            <h3 class="task-title">${esc(task.title)}</h3>
            <span class="badge badge-${task.status}">
                ${ICON[task.status]} ${LABEL[task.status]}
            </span>
        </div>
        ${task.description
            ? `<p class="task-desc">${esc(task.description)}</p>`
            : ''}
        <div class="task-footer">
            <time class="task-date">${fmtDate(task.created_at)}</time>
            <div class="task-actions">
                <button class="btn-icon btn-edit"
                        onclick="openEdit(${task.id})" title="Editar">✏️ Editar</button>
                <button class="btn-icon btn-delete"
                        onclick="deleteTask(${task.id})" title="Eliminar">🗑️ Eliminar</button>
            </div>
        </div>
    </article>`;
}

// ── Estadísticas ──────────────────────────────────────────────────────────────

async function refreshStats() {
    try {
        const all = await apiFetch('GET', '/tasks');
        const c = { pending: 0, in_progress: 0, completed: 0 };
        all.forEach(t => { if (c[t.status] !== undefined) c[t.status]++; });
        document.getElementById('stats-bar').innerHTML = `
            <span class="stat">📋 Total&nbsp;<strong>${all.length}</strong></span>
            <span class="stat">⏳ Pendientes&nbsp;<strong>${c.pending}</strong></span>
            <span class="stat">🔄 En progreso&nbsp;<strong>${c.in_progress}</strong></span>
            <span class="stat">✅ Completadas&nbsp;<strong>${c.completed}</strong></span>`;
    } catch (_) { /* silencioso */ }
}

// ── Cargar tareas ─────────────────────────────────────────────────────────────

async function loadTasks() {
    const container = document.getElementById('tasks-container');
    container.innerHTML = '<p class="state-msg">Cargando…</p>';
    try {
        const url   = currentFilter ? `/tasks?status=${currentFilter}` : '/tasks';
        const tasks = await apiFetch('GET', url);
        container.innerHTML = tasks.length
            ? tasks.map(taskCard).join('')
            : '<p class="state-msg empty">No hay tareas. ¡Crea una nueva! 🎯</p>';
        refreshStats();
    } catch (e) {
        container.innerHTML =
            `<p class="state-msg error">Error al cargar: ${esc(e.message)}</p>`;
    }
}

// ── Crear tarea ───────────────────────────────────────────────────────────────

document.getElementById('task-form').addEventListener('submit', async e => {
    e.preventDefault();
    const title = document.getElementById('task-title').value.trim();
    if (!title) { notify('El título es requerido', 'error'); return; }

    try {
        await apiFetch('POST', '/tasks', {
            title,
            description: document.getElementById('task-description').value.trim(),
            status:      document.getElementById('task-status').value
        });
        document.getElementById('task-title').value       = '';
        document.getElementById('task-description').value = '';
        document.getElementById('task-status').value      = 'pending';
        await loadTasks();
        notify('Tarea creada exitosamente ✅', 'success');
    } catch (e) {
        notify(e.message, 'error');
    }
});

// ── Eliminar tarea ────────────────────────────────────────────────────────────

async function deleteTask(id) {
    if (!confirm('¿Eliminar esta tarea?')) return;
    try {
        await apiFetch('DELETE', `/tasks/${id}`);
        await loadTasks();
        notify('Tarea eliminada', 'success');
    } catch (e) {
        notify(e.message, 'error');
    }
}

// ── Modal edición ─────────────────────────────────────────────────────────────

function openEdit(id) {
    const t = cache[id];
    if (!t) return;
    document.getElementById('edit-id').value          = t.id;
    document.getElementById('edit-title').value       = t.title;
    document.getElementById('edit-description').value = t.description || '';
    document.getElementById('edit-status').value      = t.status;
    document.getElementById('edit-modal').classList.remove('hidden');
    document.getElementById('edit-title').focus();
}

function closeModal() {
    document.getElementById('edit-modal').classList.add('hidden');
}

document.getElementById('cancel-btn').addEventListener('click', closeModal);
document.getElementById('edit-modal').addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

document.getElementById('save-btn').addEventListener('click', async () => {
    const id    = document.getElementById('edit-id').value;
    const title = document.getElementById('edit-title').value.trim();
    if (!title) { notify('El título es requerido', 'error'); return; }

    try {
        await apiFetch('PUT', `/tasks/${id}`, {
            title,
            description: document.getElementById('edit-description').value.trim(),
            status:      document.getElementById('edit-status').value
        });
        closeModal();
        await loadTasks();
        notify('Tarea actualizada ✅', 'success');
    } catch (e) {
        notify(e.message, 'error');
    }
});

// ── Filtros ───────────────────────────────────────────────────────────────────

document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.status;
        loadTasks();
    });
});

// ── Notificaciones ────────────────────────────────────────────────────────────

function notify(msg, type = 'info') {
    document.querySelectorAll('.notif').forEach(n => n.remove());
    const n = document.createElement('div');
    n.className   = `notif notif-${type}`;
    n.textContent = msg;
    document.body.appendChild(n);
    setTimeout(() => n.remove(), 3200);
}

// ── Init ──────────────────────────────────────────────────────────────────────

loadTasks();
