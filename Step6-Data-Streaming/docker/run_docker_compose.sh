#!/bin/bash

echo "Running Docker Compose for Spark and Kafka..."

docker-compose up -d -f docker-full-compose.yml

echo "Services started. You can access Spark Master UI at http://localhost:8080"

echo "To stop the services, run: docker-compose down"
