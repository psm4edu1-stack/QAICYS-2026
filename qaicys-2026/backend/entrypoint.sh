#!/bin/sh
set -eu

attempt=1
until python manage.py migrate --noinput; do
    if [ "$attempt" -ge 30 ]; then
        echo "Unable to connect to the host PostgreSQL database after 30 attempts." >&2
        exit 1
    fi
    echo "Host PostgreSQL is unavailable; retrying in 2 seconds ($attempt/30)." >&2
    attempt=$((attempt + 1))
    sleep 2
done

python manage.py collectstatic --noinput

exec "$@"
