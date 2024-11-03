#!/bin/bash

SPRING_CONTAINER_NAME="spring-backend-prod"
DJANGO_CONTAINER_NAME="django-prod"
DB_CONTAINER_NAME="sus-db-prod"
DB_USER="sample"
DB_NAME="sample"
DATA_SQL_PATH="data.sql"
DATA_SCHEMA_PATH="schema.sql"

echo "Starting Docker Compose services..."

docker compose up -d postgres --wait
#docker exec -i "$DB_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"


docker cp "$DATA_SCHEMA_PATH" "$DB_CONTAINER_NAME":/schema.sql
#docker exec -i "$DB_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -f /schema.sql

#docker compose up -d --wait

echo "All services are up and running."




# load data.sql into project
echo "Loading data into the database from data.sql..."
docker cp "$DATA_SQL_PATH" "$DB_CONTAINER_NAME":/data.sql
docker exec -i "$DB_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -f /data.sql
echo "Process completed successfully."
