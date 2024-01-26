#!/bin/bash

# Navigate to the Docker folder
cd docker

# Start Spark Master and Spark Worker
docker-compose up -f docker-bitnami-compose.yml -d spark-master spark-worker

# Wait for Spark Master and Worker to be ready (adjust sleep time as needed)
sleep 15

# Start Kafka (if not already running)
docker-compose up -d kafka

# Wait for Kafka to be ready (adjust sleep time as needed)
sleep 15

# Check if the Kafka topic exists before creating it
topic_exists=$(docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --list --topic ozkary-topic --bootstrap-server localhost:9092 | grep "ozkary-topic")

if [ -z "$topic_exists" ]; then
  # Create Kafka topic
  docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic ozkary-topic --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
  echo "Kafka topic created!"
else
  echo "Kafka topic already exists, no need to recreate."
fi

echo "Services started successfully!"
