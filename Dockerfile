# ── Stage 1: dependencias ────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /build

# Solo copiamos requirements para aprovechar cache de capas
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

LABEL maintainer="DevOps V&V Project"
LABEL description="Task Manager – Flask backend"

# Usuario sin privilegios para seguridad
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copiar dependencias compiladas desde builder
COPY --from=builder /install /usr/local

# Copiar código de la aplicación
COPY app/     ./app/
COPY run.py   .

# Directorio de datos persistentes (DB SQLite)
RUN mkdir -p /data && chown appuser:appgroup /data

# Exponer puerto de la aplicación
EXPOSE 5000

# Healthcheck interno
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

USER appuser

CMD ["python", "run.py"]
