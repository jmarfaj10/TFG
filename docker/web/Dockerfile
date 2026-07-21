# ─── Web Django (vis_go) — corre en el PC ────────────────────────────
# Contexto de build = raíz del repo (~/TFG). NO se copia el venv app/env
# (es enorme y mezcla paquetes de ROS): se instala limpio desde requirements.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias primero (mejor caché de capas)
COPY docker/web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proyecto Django (app/vis_go/ contiene manage.py)
COPY app/vis_go/ .

EXPOSE 8000

# Aplica migraciones y arranca el servidor de desarrollo.
# Para producción: gunicorn vis_go.wsgi:application --bind 0.0.0.0:8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
