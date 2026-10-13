FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --system qaicys && useradd --system --gid qaicys --home-dir /app qaicys

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

COPY backend /app/backend
COPY registration-numbers.json /app/registration-numbers.json

RUN chmod +x /app/backend/entrypoint.sh \
    && chown -R qaicys:qaicys /app

USER qaicys
WORKDIR /app/backend

EXPOSE 8000

ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8005", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]
