#!/bin/bash

# Step 1: Create Kafka Configuration File
./bash config_kafka.sh

# Step 2: Install Docker
sudo apt update
sudo apt install docker.io

# Step 3: Pull Docker Images
docker pull ozkary/kafka:mta-de-101
docker pull ozkary/spark:mta-de-101

# Step 4: Run Docker Containers (Adjust the parameters based on your needs)
docker run -d --name kafka-container -p 9092:9092 -v ~/.kafka:/config ozkary/kafka:mta-de-101
docker run -d --name spark-container -v ~/.kafka:/config ozkary/spark:mta-de-101

echo "Deployment and container setup complete!"
