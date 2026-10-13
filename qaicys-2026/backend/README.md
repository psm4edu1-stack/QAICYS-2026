# QAICYS registration backend

The root directory remains the static frontend. This directory contains the Django API and manager dashboard.

## Local setup

1. Create PostgreSQL database `event_registration` and a database user.
2. Create and activate a virtual environment.
3. Install dependencies and create the local environment file:

```bash
cd backend
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

4. Update `.env` with the PostgreSQL password and a long random `SECRET_KEY`.
5. Apply migrations and create the manager account:

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

6. From the repository root, serve the static frontend on its configured development origin:

```bash
python -m http.server 3000
```

Open `http://localhost:3000`. The manager login is at `http://127.0.0.1:8000/manager/login/`.

## Production

Set `DEBUG=False`, use a strong `SECRET_KEY`, and set PostgreSQL credentials. Set `ALLOWED_HOSTS` to the backend host and allow only the deployed frontend in `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`. The known frontend is `https://qaicys-2026.vercel.app`; the backend domain must be supplied when it is deployed.

Update the single production API placeholder in the root `api-config.js` to that HTTPS backend origin. Never use an allow-all CORS setting.

The specification contains both `Team Lead Name` and a separate `Team Lead` field for Bid Byte. Both are preserved. Until the organizers provide a more specific meaning, the second value is stored verbatim in `team_lead` rather than silently treating it as another field.

Run before deployment:

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic --noinput
```

The application requires PostgreSQL at runtime. SQLite is used only by `backend.test_settings` for isolated automated tests.

### Docker Compose production setup

The root `Dockerfile` builds only the Django API/dashboard image. PostgreSQL runs directly on the host machine and is not managed by Docker. The frontend remains deployable as the existing static Vercel project.

```bash
cp backend/.env.production.example backend/.env.production
# Replace every placeholder in backend/.env.production first.
docker compose build
docker compose up -d
docker compose exec backend python manage.py createsuperuser
docker compose ps
```

The backend health endpoint is `/health/`. At startup, the container connects to the host PostgreSQL server, applies migrations, collects hashed/compressed static dashboard assets, and starts Gunicorn as a non-root user.

Inside the container, `host.docker.internal` resolves to the host machine. The Compose file includes Docker's `host-gateway` mapping for Linux. PostgreSQL must listen on an address accessible from Docker, permit the Docker bridge network in `pg_hba.conf`, and allow its configured port through the host firewall. Do not expose PostgreSQL publicly.

Terminate services without deleting PostgreSQL data:

```bash
docker compose down
```

Production must put the backend behind an HTTPS reverse proxy or managed load balancer. Point `api.your-domain.com` to port 8000 internally, configure TLS at the proxy, then replace the placeholder in the root `api-config.js` with that HTTPS API origin. Back up the host PostgreSQL database before upgrades.

## Tests

```bash
DEBUG=True SECRET_KEY=test-only .venv/bin/python manage.py test --settings=backend.test_settings
```
