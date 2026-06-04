#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# healthcheck.sh – Verifica que la aplicación esté respondiendo
# Uso: ./scripts/healthcheck.sh [host] [port] [max_retries]
#      Defaults: localhost  5000  5
# ─────────────────────────────────────────────────────────────────────────────

HOST="${1:-localhost}"
PORT="${2:-5000}"
MAX_RETRIES="${3:-5}"
WAIT_SECONDS=3

URL="http://${HOST}:${PORT}/api/health"

echo "============================================================"
echo " Healthcheck: $URL"
echo " Reintentos máximos: $MAX_RETRIES"
echo "============================================================"

for i in $(seq 1 "$MAX_RETRIES"); do
    echo " Intento $i/$MAX_RETRIES ..."

    if curl -sf --max-time 5 "$URL" -o /dev/null 2>/dev/null; then
        RESPONSE=$(curl -s --max-time 5 "$URL" 2>/dev/null)
        echo " Respuesta: $RESPONSE"
        echo "============================================================"
        echo " RESULTADO: Servicio disponible en $URL"
        echo "============================================================"
        exit 0
    fi

    if [ "$i" -lt "$MAX_RETRIES" ]; then
        echo " Servicio no disponible, esperando ${WAIT_SECONDS}s ..."
        sleep "$WAIT_SECONDS"
    fi
done

echo "============================================================"
echo " ERROR: Servicio no disponible después de $MAX_RETRIES intentos"
echo "============================================================"
exit 1
