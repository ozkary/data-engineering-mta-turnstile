
# Data Engineering Design

A data engineering design is the actual plan to build the technical solution. It includes the system architecture, data integration, flow and pipeline orchestration, the data storage platform, transformation and management, data processing and analytics tooling. This is the area where we need to clearly define the different technologies that should be used for each area. 

#### System Architecture

The system architecture is a high-level design of the solution, its components and how they integrate with each other. This often includes the data sources, data ingestion resources, workflow and data orchestration resources and frameworks, storage resources, data services for data transformation and continuous data ingestion and validation, and data analysis and visualization tooling.

#### Data Pipelines 

A data pipeline refers to a series of connected tasks that handles the extract, transform and load (ETL) as well as the extract, load and transform (ELT)  operations and integration from a source to a target storage like a data lake or data warehouse. 

The use of ETL or ELT depends on the design. For some solutions, a flow task may transform the data prior to loading it into storage. This approach tends to increase the amount of python code and hardware resources used by the hosting environment. For the ELT process, the transformation may be done using SQL code and the data warehouse resources, which often tend to perform great for big data scenarios.

#### Data Orchestration

Data orchestration refers to the automation, management and coordination of the data pipeline tasks. It involves the scheduling, workflows, monitoring and recovery of those tasks. The orchestration ensures the execution of those tasks, and it takes care of error handling, retry and the alerting of problems in the pipeline.

### Source Control and Deployment

It is important to properly define the tooling that should be used for source control and deployments automation. The area of source code should include the Python code, Terraform, Docker configuration as well as any deployment automation scripts.

#### Source Control

Client side source control systems such as Git help in tracking and maintaining the source code for our projects. Cloud side systems such as GitHub should be used to enable the team to push their code and configuration changes to a remote repository, so it can be shared with other team members.

#### Continuous Integration and Continuous Delivery (CI/CD)

 A remote code repository like GitHub also provides deployment automation pipelines that enable us to push changes to other environments for testing and finally production releases.  

Continuous Integration (CI) is the practice to continuously integrate the code changes into the central repository, so it can be built and tested to validate the latest change and provide feedback in case of problems. Continuous Deployment (CD) is the practice to automate the deployment of the latest code builds to other environments like staging and production.

#### Docker Containers and Docker Hub

When deploying a new build, we need to also deploy the environment dependencies to avoid any run-time errors. Docker containers enable us to automate the management of the application by creating a self-contained environment with the build and its dependencies. A data pipeline can be built and imported into a container image, which should contain everything needed for the pipeline to reliably execute.

Docker Hub is a container registry which allows us to push our pipeline images into a cloud repository. The goal is to provide the ability to download those images from the repository as part of the new environment provisioning process.

### Terraform for Cloud Infrastructure

Terraform is an Infrastructure as Code (IaC) tool that enables us to manage cloud resources across multiple cloud providers. By creating resource definition scripts and tracking them under version control, we can automate the creation, modification and deletion of resources. Terraform tracks the state of the infrastructure, so when changes are made, they can be applied to the environments as part of a CI/CD process. 

![ozkary-data-engineering-design-planning-docker-terraform](../images/ozkary-data-engineering-design-terraform-docker.png "Data Engineering Process Fundamentals- Design and Planning Docker Terraform")

# Cloud Infrastructure Planning

A very important step in any technical project is to do some infrastructure planning. This is basically defining the technologies to use to successfully deliver our project. Since this is a Data Engineering project, we basically need the following resources:

- VM instance
    - To host our data pipelines and orchestration
- Data Lake 
    - To store the CSV or Parquet files
- Data Warehouse
  - To host the data to make it available to the visualization tools
      
We are building a cross-cloud platform solution, so we stick with technologies that are available in all cloud platforms. In addition, we can use Terraform to build the resources. Terraform is an open-source tool that enables us to manage infrastructure. It works with all cloud platforms. This tool enables us to create Continuous Integration Continuous Deployment (CICD) processes to manage our resources.

<img src="../images/data-engineering-terraform.png" alt="ozkary terraform"/>

## How to Run it!

**Note: for this execution plan, we are using a GCP cloud project.**

### Requirements

<a target="_gcp" href="https://github.com/ozkary/data-engineering-mta-turnstile/wiki/Google-Cloud-Configuration-Notes">GCP Configuration Notes</a>

- Setup your GCP cloud project 
  - Cloud Provider account: https://console.cloud.google.com/
  - Create the service account with permissions   
  - Install the GCP SDK

<a target="_terraform" href="https://github.com/ozkary/data-engineering-mta-turnstile/wiki/Terraform-Configuration">Terraform Configuration Notes</a>

- Install Terraform
  - https://www.terraform.io/downloads


### Execution

- Refresh service-account's auth-token for this session
```
$ gcloud auth application-default login

```

- Set the credentials file on the bash configuration file
  - Edit the bash file

```
$ nano ~/.bashrc
```

- Add the export line and replace filename-here with your file
``` 
 export GOOGLE_APPLICATION_CREDENTIALS="${HOME}/.gcp/filename-here.json"
 ```
- Save the file and exit

- Open the terraform folder in your project

> [Azure Data Lake Configuration](https://github.com/ozkary/data-engineering-mta-turnstile/wiki/Terraform-Create-an-Azure-Data-Lake)

- Initialize state file (.tfstate) one time run which should create main.tf
```
$ cd ./terraform
$ terraform init
```
-  Check changes to new infrastructure plan

> Get the project id from your GCP cloud console

```  
$ terraform plan -var="project=<your-gcp-project-id>"
```

- Apply the changes
```
$ terraform apply -var="project=<your-gcp-project-id>"
```

- (Optional) Delete infrastructure after your work, to avoid costs on any running services

```
$ terraform destroy
```

#### Terraform Lifecyle

![ozkary-data-engineering-terraform-lifecycle](../images/ozkary-data-Engineering-terraform-lifecycle.png "Data Engineering Process - Terraform Lifecycle")


### GitHub Action

> [Configure GitHub Secrets](https://github.com/ozkary/data-engineering-mta-turnstile/wiki/GitHub-Configure-Secrets-for-Build-Actions)


This is an example of a GitHub Action workflow YAML file:

```

name: Terraform Deployment

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v2
    
    - name: Set up Terraform
      uses: hashicorp/setup-terraform@v1
    
    - name: Terraform Init
       env:        
        GOOGLE_APPLICATION_CREDENTIALS:  ${{ secrets.GOOGLE_APPLICATION_CREDENTIALS }}
      run: |
        cd Step2-Cloud-Infrastructure/terraform
        terraform init
    
    - name: Terraform Apply
      run: |
        cd path/to/terraform/project
        terraform apply -auto-approve
```

> 👉 [Data Pipeline and Orchestration](https://github.com/ozkary/data-engineering-mta-turnstile/tree/main/Step3-Orchestration)