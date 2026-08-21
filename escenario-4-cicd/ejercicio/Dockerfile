# ---------- Etapa 1: build ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Etapa 2: produccion ----------
FROM python:3.11-slim AS production

WORKDIR /app

# Usuario sin privilegios (buena practica de seguridad)
RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /install /usr/local
COPY src/main.py .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status == 200 else 1)"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]