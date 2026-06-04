#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# install.sh – Instala todas las dependencias del proyecto
# Uso: ./scripts/install.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo " Task Manager – Instalación de dependencias"
echo "============================================================"
echo " Directorio raíz: $ROOT"
cd "$ROOT"

# ── Verificar Python 3 ────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 no encontrado. Instálalo antes de continuar."
    exit 1
fi
echo " Python:  $(python3 --version)"

# ── Crear entorno virtual si no existe ───────────────────────────────────────
if [ ! -d ".venv" ]; then
    echo " Creando entorno virtual .venv ..."
    python3 -m venv .venv
else
    echo " Entorno virtual .venv ya existe."
fi

# ── Activar entorno virtual ───────────────────────────────────────────────────
# shellcheck source=/dev/null
source .venv/bin/activate
echo " Entorno virtual activado."

# ── Actualizar pip ────────────────────────────────────────────────────────────
pip install --upgrade pip -q

# ── Instalar dependencias ─────────────────────────────────────────────────────
echo " Instalando dependencias desde requirements.txt ..."
pip install -r requirements.txt

echo ""
echo " Dependencias instaladas correctamente."
echo "============================================================"
