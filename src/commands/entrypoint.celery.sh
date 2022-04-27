#!/bin/sh

echo "Waiting for Postgres..."
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 0.1
done
echo "Postgres started"

echo "Waiting for RabbitMQ..."
while ! nc -z "$BROKER_HOST" "$BROKER_PORT"; do
  sleep 0.1
done
echo "RabbitMQ started"

echo "Waiting for Redis..."
while ! nc -z "$RESULT_BACKEND_HOST" "$RESULT_BACKEND_PORT"; do
  sleep 0.1
done
echo "Redis Started"

celery -A apps.config worker --loglevel=debug --concurrency=10

exec "$@"
