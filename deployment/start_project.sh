#!/bin/bash

read -p "Please enter the environment (prod/dev): " ENVIRONMENT

# Convert input to lowercase
ENVIRONMENT=$(echo "$ENVIRONMENT" | tr '[:upper:]' '[:lower:]')

# Validate the input
if [[ "$ENVIRONMENT" != "prod" && "$ENVIRONMENT" != "dev" ]]; then
  echo "Invalid environment. Please enter 'prod' or 'dev'."
  exit 1
fi


SPRING_CONTAINER_NAME="spring-backend-$ENVIRONMENT"
DJANGO_CONTAINER_NAME="django-$ENVIRONMENT"
DB_CONTAINER_NAME="sus-db-$ENVIRONMENT"

DB_USER="sample"
DB_NAME="postgres"
DATA_SQL_PATH="../data/inital_data.sql"
DATA_SCHEMA_PATH="../data/schema.sql"

echo "Starting Docker Compose services..."

cd $ENVIRONMENT

docker network create sus-network

docker compose up -d "db" --wait
sleep 10
docker exec -i "$DB_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

docker cp "$DATA_SCHEMA_PATH" "$DB_CONTAINER_NAME":/schema.sql
docker exec -i "$DB_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -f /schema.sql


echo "Loading data into the database from data.sql..."
docker cp "$DATA_SQL_PATH" "$DB_CONTAINER_NAME":/data.sql
docker exec -i "$DB_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -f /data.sql

docker compose up -d --wait
