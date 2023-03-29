# Step 4 Data Warehouse and Data Modeling

After defining a data pipeline orchestration process, we need to define how to store the data, so it can become available to visualization and analysis tools. A Data Lake is a great location to store large amounts of data, but it is not designed to allow the reading of information. For that purpose, we need to use a Data Warehouse (DW), which is an Online Analytical Processing (OLAP) tool. 

Unlike the ELT process that is used by Data Lakes, a DW uses the ETL process. This basically mean that the DW should have well-defined and optimized models, so the information can be accessed with great performance. 

Before we start building tables, we need to first create our models based on our initial analysis and requirements. We would like to use a tool that enable us to build our models in a way that it can be automated, testable and repeatable. Once we add, this process into our project, our architecture should now look as follows:

<img width="780px" src="../images/mta-data-warehouse.png" alt="ozkary data warehouse architecture"/>

## Data Modeling

We are using dbt (data build tools) to build the data analysis resources on BigQuery. With this tool, we can define the lookup, facts and dimensions table in a way that enables us to support a CICD process by rebuilding the project resources and pushing the changes to the cloud hosting environment.

- Use dbt as a model tool to create the optimized models
  - Create a seed table to be able to get the source for the lookup values
    - remote_booth_station
  - Create an external table using the Data Lake folder and parquet files as a source
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

## How to Run It

**Note: For this execution plan, we are using dbt cloud and GitHub**

### Requirements

- dbt account
  - Run the process from dbt cloud 
  - Or install locally (VM) and run from CLI
- GitHub account
- Googl BigQuery resource 

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

<img width="780px" src="../images/mta-bdt-lineage.png" alt="ozkary dbt model lineage"/>


### dbt Commands on the dbt cloud command line (browser)

-  install dbt and add the package dependencies in the packages.yml (root folder)   

```
$ pip install dbt-core dbt-bigquery
$ dbt init
$ dbt deps 
```  
  
```
    packages:
    - package: dbt-labs/dbt_utils
        version: 0.8.0
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

- Validate the project. There should be no errors
```
$ dbt debug
```

- Generate documentation 
```
$ dbt docs generate
```

- To see the project folder configuration
```
$ dbt debug --config-dir
```

