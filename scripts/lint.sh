#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# lint.sh – Analiza calidad de código con flake8
# Uso: ./scripts/lint.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo " Task Manager – Análisis de calidad de código (flake8)"
echo "============================================================"
cd "$ROOT"

# ── Activar entorno virtual si existe ────────────────────────────────────────
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

# ── Verificar que flake8 esté instalado ───────────────────────────────────────
if ! python3 -m flake8 --version &>/dev/null; then
    echo "ERROR: flake8 no instalado. Ejecuta primero scripts/install.sh"
    exit 1
fi

echo " Analizando app/ ..."
python3 -m flake8 app/

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo " Sin errores de estilo detectados."
    echo "============================================================"
    echo " RESULTADO: Código cumple estándares de calidad."
    echo "============================================================"
else
    echo "============================================================"
    echo " RESULTADO: Se encontraron errores de estilo (código: $EXIT_CODE)"
    echo "============================================================"
fi

exit $EXIT_CODE
