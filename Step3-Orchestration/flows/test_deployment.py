#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

from datetime import timedelta, date
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.deployments import Deployment

# cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
@task(name='get_file_date', description='Resolves the last file drop date')    
def get_file_date() -> str:
    curr_date = date.today()
    if curr_date.weekday() != 5:
        days_to_sat = (curr_date.weekday() - 5) % 7
        curr_date = curr_date - timedelta(days=days_to_sat)
        
    year_tag = str(curr_date.year)[2:4]
    file_name = f'{year_tag}{curr_date.month:02}{curr_date.day:02}'
    return file_name
           

@flow(name="MTA Test", description="MTA Deployment Test",log_prints=True, persist_result=False)
def test(name : str = 'yyMMdd', day: int = 0):
    if (day == 0):
        name = get_file_date()

    print(f"test: Filename {name} Deployment")

def deploy():
    deployment = Deployment.build_from_flow(
        flow=test,
        name="prefect-test-deployment"        
    )
    deployment.apply()

if __name__ == "__main__":
    deploy()