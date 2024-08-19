from prefect import flow, task
from prefect_dbt import DbtCoreOperation

@task(name="Extract Dim Station", description="Extract dimension data for stations")
def extract_dim_station():
    dbt_run = DbtCoreOperation(
        commands=["dbt run --model dim_station.sql"],
        stream_output=True
    )
    dbt_run.run()

@task(name="Extract Dim Booth", description="Extract dimension data for booths")
def extract_dim_booth():
    dbt_run = DbtCoreOperation(
        commands=["dbt run --model dim_booth.sql"],
        stream_output=True
    )
    dbt_run.run()

@task(name="Load Fact Turnstile", description="Load fact data for turnstile")
def load_fact_turnstile():
    dbt_run = DbtCoreOperation(
        commands=["dbt run --select fact_turnstile.sql"],
        stream_output=True
    )
    dbt_run.run()

@flow(name="MTA Data Transformation", description="Orchestrates the MTA data transformation process")
def main_flow():
    extract_dim_station()
    extract_dim_booth()
    load_fact_turnstile()

if __name__ == "__main__":
    main_flow()
