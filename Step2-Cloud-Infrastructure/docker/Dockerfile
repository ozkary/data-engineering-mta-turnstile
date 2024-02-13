# pull an image with prefect and python
FROM prefecthq/prefect:2.7.7-python3.9

# copy the dependency file
COPY docker-requirements.txt .

# install dependencies
RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

# build the folders in the container
RUN mkdir -p /opt/prefect/data/
RUN mkdir -p /opt/prefect/flows/

# copy source code into the container
COPY flows opt/prefect/flows

# copy any seeding data
# COPY data opt/prefect/data