#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# test.sh – Ejecuta la suite de pruebas en ambiente test aislado
# Uso: ./scripts/test.sh [pytest-args...]
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo " Task Manager – Ejecución de pruebas"
echo "============================================================"
cd "$ROOT"

# ── Configurar ambiente de test ───────────────────────────────────────────────
export APP_ENV=test
export DEBUG=false
export DATABASE_PATH="/tmp/taskmanager_test_$$.db"

echo " APP_ENV:       $APP_ENV"
echo " DATABASE_PATH: $DATABASE_PATH"
echo ""

# ── Activar entorno virtual si existe ────────────────────────────────────────
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

# ── Función de limpieza al salir ──────────────────────────────────────────────
cleanup() {
    rm -f "$DATABASE_PATH" 2>/dev/null || true
    echo ""
    echo " Base de datos temporal eliminada."
}
trap cleanup EXIT

# ── Ejecutar pytest ───────────────────────────────────────────────────────────
if [ $# -gt 0 ]; then
    python3 -m pytest "$@"
else
    python3 -m pytest
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "============================================================"
    echo " RESULTADO: Todas las pruebas pasaron correctamente."
    echo "============================================================"
else
    echo "============================================================"
    echo " RESULTADO: FALLARON pruebas (código de salida: $EXIT_CODE)"
    echo "============================================================"
fi

exit $EXIT_CODE
