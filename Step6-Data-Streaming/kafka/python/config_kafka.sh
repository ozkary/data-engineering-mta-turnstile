#!/bin/bash
# run this on the target VM
CONFIG_DIR=~/.kafka
CONFIG_FILE=$CONFIG_DIR/docker-kafka.properties

# Set Kafka host (replace localhost with your actual Kafka host if it is not running locally)
DOCKER_KAFKA_HOST=localhost

# Check if the .kafka directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating $CONFIG_DIR directory..."
    mkdir -p "$CONFIG_DIR"
fi


# Check if the Kafka configuration file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Creating $CONFIG_FILE..."
    cat <<EOL > "$CONFIG_FILE"
bootstrap.servers=$DOCKER_KAFKA_HOST:9092
# Add other Kafka configuration properties as needed
EOL
    echo "Kafka configuration file created successfully."
else
    echo "$CONFIG_FILE already exists. Skipping creation."
fi