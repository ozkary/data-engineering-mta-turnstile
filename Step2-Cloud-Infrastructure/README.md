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

- Initialize state file (.tfstate) one time run which should create main.tf
```
$ cd ./terraform
$ terraform init
```
-  Check changes to new infrastructure plan
```  
$ terraform plan -var="project=<your-gcp-project-id>"
```

# Apply the changes
```
$ terraform apply -var="project=<your-gcp-project-id>"
```

- (Optional) Delete infrastructure after your work, to avoid costs on any running services

```
$ terraform destroy
```



