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

# Specify the default command to run when the container starts
CMD ["python3", "program.py", "--topic","mta-turnstile","--config","/config/docker-kafka.properties"]

# Create a directory for Kafka configuration
RUN mkdir -p /config

# Create a volume mount for Kafka configuration
VOLUME ["/config"]

# push the ~/.kafka/docker-kafka.properties to the target machine
# run as to map the volume to the target machine:
# docker run -v ~/.kafka:/config your-image-name
