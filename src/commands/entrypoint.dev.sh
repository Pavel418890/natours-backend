#!/bin/sh

echo "Starting natours server..."
echo "Waiting for postgres..."

while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
    sleep 0.1
done
echo "PostgreSQL started"

python manage.py collectstatic --no-input --clear

# check relationship in database is correct
python manage.py migrate

# make sure that a reports and views exist
cp \
 /home/app/src/apps/natours/create_db_view_migrations.py \
 /home/app/src/apps/natours/migrations/

python manage.py migrate

# run server
python manage.py runserver 0.0.0.0:8888

exec "$@"
