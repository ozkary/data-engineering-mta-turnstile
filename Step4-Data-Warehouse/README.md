# Step 4 Data Warehouse and Data Modeling

After defining a data pipeline orchestration process, we need to define how to store the data, so it can become available to visualization and analysis tools. A Data Lake is a great location to store large amounts of data, but it is not designed to allow the reading of information. For that purpose, we need to use a Data Warehouse (DW), which is an Online Analytical Processing (OLAP) tool. 

Unlike the ELT process that is used by Data Lakes, a DW uses the ETL process. This basically mean that the DW should have well-defined and optimized models, so the information can be accessed with great performance. 

Before we start building tables, we need to first create our models based on our initial analysis and requirements. We would like to use a tool that enable us to build our models in a way that it can be automated, testable and repeatable. Once we add, this process into our project, our architecture should now look as follows:

<img width="780px" src="../images/mta-data-warehouse.png" alt="ozkary data warehouse architecture"/>

## Data Modeling

We are using cloud data build tools (dbt) to build the data analysis resources on BigQuery. With this tool, we can define the lookup, facts and dimensions table in a way that enables us to support a CICD process by rebuilding the project resources and pushing the changes to the cloud hosting environment. Another great tool for data modeling between a data lake and data warehouse is Apache Spark.

> [Use cloud dbt for a SQL like approach](https://www.getdbt.com/)

> [Use Apache Spark when using Python or need data streaming](https://spark.apache.org/)

<a target="_dbt" href="https://github.com/ozkary/data-engineering-mta-turnstile/wiki/Configure-dbt-CLI">Read dbt CLI Configuration to use your terminal instead of dbt cloud</a>


- Use dbt as a model tool to create the optimized models
  - Create a seed table to be able to get the source for the lookup values
    - remote_booth_station
  - Create an external table using the Data Lake folder and CSV.gz files as a source
    - ext_turnstile
  - Create the dimension tables using the lookup values as source
    - dim_station
    - dim_booth
       - Cluster by station_id
    - Add incremental model to insert missing records not on seed table
  - Create the fact table using the external table structure and an incremental strategy for ongoing new data
    - fact_turnstile
    - Partition the table by created_dt and day granularity
    - Cluster the table by station_id
    - Join on dimension tables to use id references instead of text
    - Continously run this model with an incremental strategy to append new records

Our data model should look like this:

<img width="680px" src="../images/mta-erd.png" alt="ozkary data warehouse ERD"/>

### Why do we use partitions and cluster

- Partitioning is the process of dividing a large table into smaller, more manageable parts based on the specified column . Each partition contains rows that share a common value like a specific date. A partition improves performance and query cost.

- When we run a query in BigQuery, it gets executed by a distributed computing infrastructure that spans multiple machines. Clustering is an optional feature in BigQuery that allows us to organize the data within each partition. The purpose of clustering is to physically arrange data within a partition in a way that is conducive to efficient query processing.

#### SQL Server and Big Query Concept Comparison

- In SQL Server, a clustered index defines the physical order of data in a table. In BigQuery, clustering refers to the organization of data within partitions based on one or more columns. Clustering in BigQuery does not impact the physical storage order like a clustered index in SQL Server.

- Both SQL Server and BigQuery support table partitioning. The purpose is similar, allowing for better data management and performance optimization. 

## How to Run It

**Note: For this execution plan, we are using dbt cloud and GitHub**

### Requirements

**Note: Make sure to run the prefect flows from step 2. That process copy files to the Data Lake.**

- CSV files in the Data Lake
- dbt account
  - Run the process from dbt cloud 
  - Link dbt with your Github project
  - Create schedule job on dbt cloud for every Sunday 9am
  - Or install locally (VM) and run from CLI
- GitHub account
- Google BigQuery resource 

**Note: Use the dbt folder**

### Create the models

  In the models folder, we create the folder and files for the process. 
  
  - staging
    This folder contains the raw data in the form of specialized views to make the different data sources uniforms. These files are used by the core files to build the
    actual tables.

    - Create the schema.yml file which provides the database connection information as well as the schema definition for the models
    - Add the models with the view materialization strategies. 
       - A view for each data source with a common field names as this goes into the fact tables
       - A view for the station dimension from the seed/lookup table
       - A view for the booth dimension from the seed/lookup table

    - core   
     This folder hosts the resources that are made available for the data analysis process. This includes the materialized fact and dimension tables

     - Add the dimension station and booth tables from the view models
     - Add the fact table with all the views as source
         - Use common table expressions to be able to join all the views
     - Add a schema.yml file to describe all the tables

### Lineage 

![ozkary-data-engineering-dbt-model-lineage](../images/mta-bdt-lineage.png "ozkary dbt model lineage")

### dbt Commands on the dbt cloud command line (browser)

-  Clone this project
-  Install dbt and add the package dependencies in the packages.yml (root folder)   
-  Use dbt init to initialize the project profile to your resources
   - Set up a dbt profile to connect to your cloud-based data warehouse. This typically involves creating a new profile in your ~/.dbt/profiles.yml file, or editing an existing profile. You should refer to the documentation for your cloud platform to determine the appropriate parameters to include in your profile.

```
$ pip install dbt-core dbt-bigquery
$ dbt init
$ dbt deps 
```  
- The packages.yml file should have the following dependency
```
    packages:
    - package: dbt-labs/dbt_utils
        version: 0.8.0
 ```

- Test your connection by running a dbt command that requires a connection to your cloud-based data warehouse, such as dbt list.
- Once you have verified that your connection is working, you can use the --profile flag to specify which profile to use for each dbt command. For example, to run dbt using the Analytics profile, you would use the command:

> The profile name is defined in the dbt_project.yml file

```
dbt list --profile Analytics
```
- Connect to your Data Warehouse 
- Create an external table using the Data Lake files as the source with the following script

**Note: This is a BigQuery example**

```
CREATE OR REPLACE EXTERNAL TABLE mta_data.ext_turnstile
OPTIONS (
  format = 'CSV',
  uris = ['gs://ozkary_data_lake_ozkary-de-101/turnstile/*.csv.gz']  
);

```

- to create the seed tables/lookup with a CSV file

```
$ dbt seed 
```

- Builds the model and uses the variable to allow for the full dataset to be created

```
$ dbt build --select stg_booth.sql --var 'is_test_run: false'
$ dbt build --select stg_station.sql --var 'is_test_run: false'
$ dbt build --select stg_turnstile.sql --var 'is_test_run: false'

$ dbt build --select dim_booth.sql 
$ dbt build --select dim_station.sql 
$ dbt build --select fact_turnstile.sql

```  
- After runnining these command, the following resources should be in the data warehouse

<img width="380px" src="../images/mta-bigquery-schema.png" alt="ozkary dbt bigquery schema"/>

> The build command is responsible for compiling, generating and deploying the SQL code for your dbt project, while the run command executes that SQL code against your data warehouse to update the data. Typically, you would run dbt build first to compile the project, and then run dbt run to execute the compiled code against the database.

- Validate the project. There should be no errors
```
$ dbt debug
```
- Run the test 
```
$ dbt test
```
<img width="780px" src="../images/mta-dbt-test.png" alt="ozkary dbt test results"/>


- Generate documentation 
```
$ dbt docs generate
```

- To see the project folder configuration
```
$ dbt debug --config-dir
```
- On dbt Cloud setup the dbt schedule job to run every Sunday at 9am
  - Use the production environment
  - Use the following command
```
$ dbt run --model fact_turnstile.sql
```

- After running the cloud job, the log should show the following

<img width="780px" src="../images/mta-dbt-job.png" alt="ozkary dbt run results"/>

**Note: There should be files on the Data Lake for the job to insert any new records. To validate this, run these queries from the Data Warehouse**

```
-- check station dimension table
select count(*) from mta_data.dim_station;

-- check booth dimension table
select count(*) from mta_data.dim_booth;

-- check the fact table
select count(*) from mta_data.fact_turnstile;

-- check the staging fact data
select count(*) from mta_data.stg_turnstile;
```

- To check the weekly new data, we can use this query.

[Query for New Incremental (only) Fact Data](sql/fact_tunstile_incremental.sql)

### Data Policies

The files from the Data Lake have an expiration policy. Files older than two weeks will be drop from storage. This should allow for the process to keep a good performance.


> 👉 [Data Analyis and Visualization](https://github.com/ozkary/data-engineering-mta-turnstile/tree/main/Step5-Analysis)