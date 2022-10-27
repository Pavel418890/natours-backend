#!/bin/sh

echo "Starting natours server..."
echo "Waiting for postgres..."

while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
    sleep 0.1
done
echo "PostgreSQL started"

python manage.py collectstatic --no-input --clear

# run server
gunicorn -w $((2 * $(nproc) + 1 )) \
  -b 0.0.0.0:80 \
  --log-level=error \
  wsgi:application

exec "$@"
