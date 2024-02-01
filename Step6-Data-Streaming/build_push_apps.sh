#!/bin/bash

# Log in to Docker Hub using environment variables
docker login --username "$DOCKER_USERNAME" --password-stdin <<< "$DOCKER_PASSWORD"

# Set the image names and tags
KAFKA_PRODUCER_IMAGE="ozkary/kafka:mta-de-101"
SPARK_CONSUMER_IMAGE="ozkary/spark:mta-de-101"

# Build Kafka producer image
echo "Building Kafka producer image..."
docker build -t $KAFKA_PRODUCER_IMAGE kafka/python/

# Push Kafka producer image to Docker Hub
echo "Pushing Kafka producer image to Docker Hub..."
docker push $KAFKA_PRODUCER_IMAGE

# Build Spark consumer image
echo "Building Spark consumer image..."
docker build -t $SPARK_CONSUMER_IMAGE spark/

# Push Spark consumer image to Docker Hub
echo "Pushing Spark consumer image to Docker Hub..."
docker push $SPARK_CONSUMER_IMAGE

echo "Build and push completed."

# Logout from to Docker Hub
docker logout
