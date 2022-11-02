#!/bin/bash


echo "Waiting for Postgres..."

while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 0.1
done

echo "Postgres started"

echo "Waiting for RabbitMQ..."

while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
  sleep 0.1
done

echo "RabbitMQ started"

celery  -A apps.config flower --concurrency=3

exec "$@"
