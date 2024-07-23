#!/bin/bash

# Navigate to the spark directory
cd spark/

# Check if the .venv directory exists
if [ ! -d ".venv" ]; then
    # Create a virtual environment
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run your Spark program using spark-submit
bash submit-program.sh program.py ~/.kafka/docker-kafka.properties

# Display a message indicating completion
echo "Spark program submitted to Spark cluster within the virtual environment."

# Deactivate the virtual environment (optional)
# deactivate
