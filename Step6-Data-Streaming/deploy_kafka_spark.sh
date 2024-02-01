#!/bin/bash

# Step 1: Install Docker
sudo apt update
sudo apt install docker.io

# Step 2: Pull Docker Images
docker-compose -f docker/docker-compose-bitnami.yml pull

# Step 3: Run Docker Containers (Adjust the parameters based on your needs)
docker-compose -f docker/docker-compose-bitnami.yml up -d

echo "System dependencies deployed and containers are running!"
