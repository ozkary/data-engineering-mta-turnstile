# Step 3 Data Orchestration

At this point of the project, we understand the source and structure of the data. We also have provisioned a Data Lake (DL) to store all the files that we need to download. We are ready to orchestrate a data pipeline that can enable us to process multiple files and save them to the DL using a compressed or parquet data format. Let’s first review some of these concepts.

A data pipeline is a workflow with different steps in which some data is extracted, processed and stored at another location. The automation, scheduling and monitor of these steps is referred to as orchestration. For this project, we are using Prefect cloud as an orchestration as a service tool.

### Orchestration Tools

> [Prefect cloud](https://www.prefect.io/)

> [Apache Airflow ](https://airflow.apache.org/)

<img src="../images/mta-orchestration.png" width="650px" alt="ozkary data engineering orchestration">

### Data Flow Process

Our basic data flow can be defined as the following:

- Download a CSV text file  
- Compress the text file and upload in chunks to the data lake
- The data transformation service picks up the file, identifies new data and inserts into the Data Warehouse.

> This data integration project fits into the batch processing model. For real-time scenarios, we should use a data streaming technologies like [Apache Kafka](https://kafka.apache.org/)

<img src="../images/mta-data-lake-bucket.png" width="650px" alt="ozkary data lake files">

### Initial Data Load

Since we need to load the data for 2023, we need to first run a batch process to load all the previous months of data. The process will not allow for the download of future data files, so an attempt to pass future dates will not be allowed.

Once the deployments is set on Prefect cloud, we can schedule jobs to download the previous months as follows:

This job downloads all the files for Jan 2023. For the following months, we change the month parameter for that month (Feb-2, Mar-3 etc)

```
$ prefect deployment run dep-docker-mta-de-101 -p "year=2023 month=1"
```

**Note: This job should be scheduled from Prefect cloud.**

### Weekly Automation

Since the files are available on a weekly basis, we use a batch processing approach to process those files. For that, we create a scheduled job with Prefect, which triggers the job with no parameter, so the flow process the most recent drop date. 

**Note: By not passing any parameters, the code resolves the last drop date and process that file.
**
```
$ prefect deployment run dep-docker-mta-de-101
```

### Monitor from Prefect Cloud

From Prefect cloud, we can monitor the flows. 

**Note:This is what a flow process looks like in Prefect Cloud.**

<img src="../images/mta-flow-run.png" width="650px" alt="ozkary prefect flow run">

### Weekly Schedule

From Prefect cloud, we can schedule weekly jobs to run every Sunday at 9am to pickup the Saturday files.

<img src="../images/mta-prefect-job.png" width="650px" alt="ozkary prefect job">

<img src="../images/mta-prefect-schedule.png" width="450px" alt="ozkary prefect job">

## How to Run It

**Note: For this execution plan, we are using Prefect cloud.**

### Requirements
- Docker and Docker hub
    - [Install Docker](https://github.com/ozkary/data-engineering-mta-turnstile/wiki/Configure-Docker)
- Prefect dependencies and cloud account
- Data Lake for storage

- Open the working directory where the requirements file is located to install the dependencies.

```
$ cd Step3*
$ pip install -r prefect-requirements.txt
```

> Make sure to run the terraform script to build the VM, datalake and BigQuery resources.

- Copy the GCP credentials to follow this format

```
$ cd ~ && mkdir -p ~/.gcp/
$ cp <path to JSON file> ~/.gcp/credentials.json
```

### Create the PREFECT Cloud Account

> API keys can be created from the user profile configuration (click your profile picture)
> 
- Login with preface cloud to host the blocks and the deployments, view the dashboards
  - preface cloud login  or use prefect cloud login -k API_KEY_FROM_PREFECT
    - This creates a key file ~/.prefect/profiles.toml
- Add a prefect block with the GCP credentials
- Run terraform plan to get the GCP resource names

### Define the resource names that are needed
- GCS bucket name
    - mta_data_lake
- Prefect Account block name
    - blk-gcp-svc-acc
- Prefect GCS (storage) block name
    - blk-gcs_name
- Prefect Deployments
    - dep-docker-mta    
- GCP BigQuery dataset name (database alias)
    - mta_data    
- Docker container name after pushing to dockerhub
    - ozkary/prefect:mta-de-101

- Copy the GCP credentials account

### Install the prefect blocks and install our custom blocks for GCP credentials and GCS access

> Blocks are a secured way to download credentials and secrets that are used by your applications.

```
$ prefect cloud login
$ prefect block register -m prefect_gcp
$ prefect block ls
$ cd ./blocks
$ python3 gcp_acc_block.py --file_path=~/.gcp/credentials.json --gcp_acc_block_name=blk-gcp-svc-acc
$ python3 gcs_block.py --gcp_acc_block_name=blk-gcp-svc-acc --gcs_bucket_name=mta_data_lake --gcs_block_name=blk-gcs-name
```

### Check the flow runs from the CLI
```
$ prefect block-run ls
```
![ozkary-data-engineering-prefec-flow-run](../images/ozkary-data-engineering-design-prefect-flows.png "Data Engineering Process Fundamentals- Prefect Flow Runs")


**Ref: https://prefecthq.github.io/prefect-gcp/**

### Create a docker image and push to DockerHub

> Make sure to run the Docker build command where the Docker file is located or use -f with the file path

```
$ docker login --username USER --password PW
$ docker image build -t ozkary/prefect:mta-de-101 .
$ docker image push ozkary/prefect:mta-de-101
```

### Create the prefect block with the docker image
```
$ cd ./blocks
$ python3 docker_block.py --block_name=blk-docker-mta-de-101 --image_name=ozkary/prefect:mta-de-101
```

### Create the prefect deployments with the docker image and start the agent
```
$ cd ./deployments
$ python3 docker_deploy_etl_web_to_gcs.py --block_name=blk-docker-mta-de-101 --deploy_name=dep-docker-mta-de-101
$ prefect deployments ls
```

### Start the Prefect Agent

The agent should be running for the scheduled deployments can be executed. This is what allows Prefect to download the container and run the code.

```
$ prefect agent start -q default
```

### Test run the prefect deployments with the docker image
```
$ prefect deployment run dep-docker-mta-de-101 -p "year=2023 month=3 day=25"
```

### Manual test run can be done from a terminal
```
$ python3 etl_web_to_gcs.py --year 2023 --month 5 --day 6
```

### GitHub Action to build and deploy the Docker image to DockerHub

> [Configure GitHub Secrets](https://github.com/ozkary/data-engineering-mta-turnstile/wiki/GitHub-Configure-Secrets-for-Build-Actions)

```

name: Build and Push Docker Image

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Login to Docker Hub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_PASSWORD }}

    - name: Build and push Docker image
      env:        
        DOCKER_REPOSITORY:  ${{ secrets.DOCKERHUB_USERNAME }}/prefect:mta-de-101
      run: |
        docker buildx create --use
        docker buildx build --push --platform linux/amd64,linux/arm64 -t $DOCKER_REPOSITORY .

```
