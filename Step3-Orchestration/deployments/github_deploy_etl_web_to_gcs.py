#!/usr/bin/env python
# coding: utf-8

import argparse
from prefect.deployments import Deployment
from etl_web_to_gcs import etl_web_to_gcs
from prefect.filesystems import GitHub 

def main(params) -> None:
    """Create a prefect deployment with github"""
    block_name = params.block_name
    deploy_name = params.deploy_name
    github_path = params.github_path    

    github_block = GitHub.load(block_name)

    deployment = Deployment.build_from_flow(
          flow=etl_web_to_gcs,
          name=deploy_name,
          storage=github_block,
          entrypoint=f"{github_path}/etl_web_to_gcs.py:etl_web_to_gcs")

    deployment.apply()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a reusable prefect deployment script')

    parser.add_argument('--block_name', required=True, help='Github block name')    
    parser.add_argument('--deploy_name', required=True, help='Prefect deployment name')    
    parser.add_argument('--github_path', required=True, help='Github folder path where the pipeline file is located')    
        
    args = parser.parse_args()

    main(args)
