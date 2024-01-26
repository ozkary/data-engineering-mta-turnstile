#!/bin/bash

echo "Downloading Spark and Kafka Docker images..."

# Spark images from Bitnami
docker pull bitnami/spark:latest

# Kafka image from Bitnami
docker pull bitnami/kafka:latest

echo "Images downloaded successfully!"

# Display image sizes
echo "Image sizes:"
docker images bitnami/spark:latest bitnami/kafka:latest --format "{{.Repository}}:{{.Tag}} - {{.Size}}"
