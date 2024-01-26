#!/bin/bash

# Navigate to the kafka directory
cd kafka/python

# Check if the .venv directory exists
if [ ! -d ".venv" ]; then
    # Create a virtual environment
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run the Kafka producer
python3 program.py --topic mta-turnstile --config ~/.kafka/docker-kafka.properties

# Display a message indicating completion
echo "Kafka producer started within the virtual environment."

# Deactivate the virtual environment (optional)
# deactivate
