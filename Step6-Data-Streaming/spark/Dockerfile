# Use a base image with Prefect and Python
FROM prefecthq/prefect:2.7.7-python3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

# Copy the entire current directory into the container
COPY *.py .
COPY *.sh .

# Create a directory for Kafka configuration
RUN mkdir -p /config

# Create a volume mount for Kafka configuration
VOLUME ["/config"]

# Set the entry point script as executable
RUN chmod +x submit-program.sh

# Specify the default command to run when the container starts
CMD ["/bin/bash", "submit-program.sh", "program.py", "/config/docker-kafka.properties"]

# push the ~/.kafka/docker-kafka.properties to the target machine
# run as to map the volumne to the target machine:
# docker run -v ~/.kafka:/config your-image-name
