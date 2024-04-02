# dbt Project

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

### dbt Commands on the dbt cloud command line (browser)

- Add the package dependencies in the packages.yml (root folder)   

```
$ dbt deps 
```  
  
```
    packages:
    - package: dbt-labs/dbt_utils
        version: 0.8.0
 ```

- To preview the build command with a row count limit

```bash
$ dbt show dim_station limit 100
```

- To create the seed tables/lookup with a CSV file

```bash
$ dbt seed --select remote_booth_station
```

- Run all the models using this pattern
```bash
$ dbt run --m <model.sql>
```

- Test your data
```bash
$ dbt test
```

- This command runs the seed, run and test at the same time
```bash
$ dbt build --select <model.sql>
```

- Builds the model and uses variables to allow for the full dataset to be created

```bash
$ dbt build --select <model.sql> --var 'is_test_run: false'
```  

- Generate documentation 
```bash
$ dbt docs generate
```

- To see the project folder configuration
```bash
$ dbt debug --config-dir
```

