# Cloud Infrastructure Planning

A very important step in any technical project is to do some infrastructure planning. This is basically defining the technologies to use to successfully deliver our project. Since this is a Data Engineering project, we basically need the following resources:

- VM instance
    - To host our data pipelines
- Data Lake 
    - To store the CSV files
- Data Warehouse
  - To host the data to make it available to visualization tools
      
We are building a cross-cloud platform solution, so we stick with technologies that are available in all cloud platforms. In addition, we can use Terraform to build the resources. Terraform is an open-source tool that enables us to manage infrastructure. It works with all cloud platforms. This tool enables us to create Continuous Integration Continuous Deployment (CICD) processes to manage our resources.

<img src="../images/data-engineering-terraform.png" alt="ozkary terraform"/>

