#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# run.sh – Levanta la aplicación en el ambiente indicado
# Uso: ./scripts/run.sh [dev|test|prod]   (default: dev)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

ENV="${1:-dev}"

# ── Validar argumento de ambiente ─────────────────────────────────────────────
if [[ ! "$ENV" =~ ^(dev|test|prod)$ ]]; then
    echo "ERROR: Ambiente inválido '$ENV'. Valores permitidos: dev, test, prod"
    exit 1
fi

echo "============================================================"
echo " Task Manager – Iniciando ambiente: $ENV"
echo "============================================================"
cd "$ROOT"

# ── Cargar variables del ambiente ─────────────────────────────────────────────
ENV_FILE=".env.$ENV"
if [ -f "$ENV_FILE" ]; then
    echo " Cargando variables desde $ENV_FILE ..."
    # Exportar solo líneas que no son comentarios
    set -o allexport
    # shellcheck source=/dev/null
    source "$ENV_FILE"
    set +o allexport
else
    echo "ADVERTENCIA: $ENV_FILE no encontrado. Usando valores por defecto."
fi

# ── Crear directorio de datos si es necesario ─────────────────────────────────
DB_DIR="$(dirname "${DATABASE_PATH:-/tmp/taskmanager.db}")"
if [ "$DB_DIR" != "." ] && [ "$DB_DIR" != "" ]; then
    mkdir -p "$DB_DIR" 2>/dev/null || true
fi

# ── Activar entorno virtual si existe ────────────────────────────────────────
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

echo " Ambiente:  ${APP_ENV:-development}"
echo " Puerto:    ${PORT:-5000}"
echo " Debug:     ${DEBUG:-true}"
echo " Base datos: ${DATABASE_PATH:-taskmanager.db}"
echo ""

python3 run.py
